"""
Iterate over priority domains and send data to server
"""
import argparse
from datetime import time
import json
import logging.config
import os
from yaasr import get_all_streams
from yaasr.recorder.stream import YStream
from yaasr.processors.audio.reduce import reformat
from yaasr.processors.archive.google_cloud import upload_to_google_cloud_storage
from yaasr.terminal.supervisor import setup_supervisor


def ls(test_streams=False):
    """ List all available streams """
    # list all streams
    streams = get_all_streams()
    for stream in streams:
        ys = YStream(stream)
        ys.load()
        print(f'{stream}: {ys.streams[0]["url"]}')
        if test_streams:
            ys.record(total_seconds=30, chunk_bytes_size=512, chunk_time_size=1000)


def info(stream):
    """ Shows stream info """
    # list all streams
    ys = YStream(stream)
    ys.load()
    data = json.dumps(ys.data, indent=4)
    print(data)


def record(stream, total_seconds=300, chunk_bytes_size=256, chunk_time_size=60):
    """ Shows stream info """
    # list all streams
    ys = YStream(stream)
    ys.load()
    ys.record(total_seconds=total_seconds, chunk_bytes_size=chunk_bytes_size, chunk_time_size=chunk_time_size)


def compress_and_google_store(stream,
                              bucket_name,
                              total_seconds=300,
                              chunk_bytes_size=256,
                              chunk_time_size=60,
                              audio_format='ogg',
                              from_time=None,
                              to_time=None):
    """ Shows stream info """

    ys = YStream(stream)
    ys.load()
    ys.post_process_functions = [
        {
            'fn': reformat,
            'params': {
                'audio_format': audio_format,
                'mono': True,
                'delete_on_success': True
            }
        },
        {
            'fn': upload_to_google_cloud_storage,
            'params': {
                'bucket_name': bucket_name,
                'delete_on_success': True
            }
        }
    ]

    if from_time is not None:
        parts = from_time.split(':')
        ys.record_from_time = time(int(parts[0]), int(parts[1]))
    if to_time is not None:
        parts = to_time.split(':')
        ys.record_to_time = time(int(parts[0]), int(parts[1]))

    ys.record(total_seconds=total_seconds, chunk_bytes_size=chunk_bytes_size, chunk_time_size=chunk_time_size)


def main():
    # TODO fix path or replace to local settings
    logging.config.fileConfig('yaasr/log.conf')
    parser = argparse.ArgumentParser()
    parser.add_argument('command', help='Command to run')
    parser.add_argument('--log_level', nargs='?', default='INFO', type=str)
    parser.add_argument('--stream', nargs='?', default=None, type=str)
    # record parameters
    parser.add_argument('--total_seconds', nargs='?', default=0, type=int)
    parser.add_argument('--chunk_bytes_size', nargs='?', default=256, type=int)
    parser.add_argument('--chunk_time_size', nargs='?', default=1200, type=int)
    parser.add_argument('--from_time', nargs='?', default=None, type=str, help="like 14:32")
    parser.add_argument('--to_time', nargs='?', default=None, type=str, help="like 14:32")
    # compress parameters
    parser.add_argument('--audio_format', nargs='?', default='mp3', choices=['mp3', 'ogg'], type=str)
    parser.add_argument('--bucket_name', nargs='?', default=None, type=str)

    # credentials
    parser.add_argument('--google-credentials', nargs='?', default=None, type=str)
    parser.add_argument('--system-user', nargs='?', default=None, type=str)

    args = parser.parse_args()

    if args.google_credentials is not None:
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = args.google_credentials

    if args.command == 'ls':
        return ls()
    elif args.command == 'test':
        return ls(test_stream=True)
    elif args.command == 'info':
        return info(stream=args.stream)
    elif args.command == 'record':
        return record(
            stream=args.stream,
            total_seconds=args.total_seconds,
            chunk_bytes_size=args.chunk_bytes_size,
            chunk_time_size=args.chunk_time_size
        )
    elif args.command == 'compress-and-google-store':
        if args.bucket_name is None:
            raise Exception('bucket name is required')

        return compress_and_google_store(
            stream=args.stream,
            bucket_name=args.bucket_name,
            total_seconds=args.total_seconds,
            chunk_bytes_size=args.chunk_bytes_size,
            chunk_time_size=args.chunk_time_size,
            audio_format=args.audio_format,
            from_time=args.from_time,
            to_time=args.to_time
        )
    elif args.command == 'supervisor':
        return setup_supervisor(
            stream_name=args.stream,
            bucket_name=args.bucket_name,
            system_user_name=args.system_user,
            google_credentials_path=args.google_credentials,
            total_seconds=args.total_seconds,
            chunk_bytes_size=args.chunk_bytes_size,
            chunk_time_size=args.chunk_time_size
        )
