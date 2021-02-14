"""
Iterate over priority domains and send data to server
"""
import argparse
import json
import logging.config
from yaasr import get_all_streams
from yaasr.recorder.stream import YStream


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


def main():
    logging.config.fileConfig('yaasr/log.conf')
    parser = argparse.ArgumentParser()
    parser.add_argument('command', help='Command to run')
    parser.add_argument('--log_level', nargs='?', default='INFO', type=str)
    parser.add_argument('--stream', nargs='?', default=None, type=str)
    parser.add_argument('--total_seconds', nargs='?', default=300, type=int)
    parser.add_argument('--chunk_bytes_size', nargs='?', default=256, type=int)
    parser.add_argument('--chunk_time_size', nargs='?', default=60, type=int)

    args = parser.parse_args()

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
            chunk_time_size=args.chunk_time_size)
