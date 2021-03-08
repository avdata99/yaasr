import json
import logging
import os
import pytz
import requests
from time import sleep
from datetime import datetime, timedelta
from yaasr import STREAMS_FOLDER
from yaasr.exceptions import StreamFolderNotFoud, StreamDataFileNotFoud


logger = logging.getLogger(__name__)


class YStream:
    """ YAASR stream """

    def __init__(self, stream_name, streams_folder=STREAMS_FOLDER, destination_folder=''):
        self.name = stream_name
        self.streams_folder = streams_folder
        self.str_chunk_time_format = '%Y-%m-%d--%H-%M-%S'
        # after save each audio chunk we can post-process the file, upload or anything
        self.post_process_functions = []
        self.short_name = self.name
        self.destination_folder = destination_folder
        self.timezone = pytz.timezone('UTC')

        # ranges to record (to avoid record 24h)
        self.record_from_time = None
        self.record_to_time = None

    def set_record_times(self, from_time=None, to_time=None):
        self.record_from_time = from_time
        self.record_to_time = to_time

    def get_stream_folder(self):
        """ Get the stream folder """
        stream_folder = os.path.join(self.streams_folder, self.name)
        if not os.path.isdir(stream_folder):
            raise StreamFolderNotFoud(f'Stream not found {stream_folder}')

        return stream_folder

    def load(self):
        """ Load and validate the stream data """
        self.stream_folder = self.get_stream_folder()
        data_file = os.path.join(self.stream_folder, 'data.json')
        if not os.path.isfile(data_file):
            raise StreamDataFileNotFoud(f'Data file not found {data_file}')

        self.data = json.load(open(data_file))

        self.title = self.data['title']
        self.web_site = self.data.get('web', None)
        self.streams = self.data['streams']
        self.short_name = self.data.get('short_name', self.name)
        self.timezone = pytz.timezone(self.data.get('timezone', 'UTC'))

    def generate_stream_path(self, extension):
        now = datetime.now(self.timezone)
        stime = now.strftime(self.str_chunk_time_format)
        stream_path = os.path.join(self.destination_folder, f'{self.short_name}-{stime}.{extension}')
        return now, stream_path

    def record(self, total_seconds=0, chunk_bytes_size=1024, chunk_time_size=60):
        """ Record the online stream

        Params:
            total_seconds: total time to save from the stream. 0 is for ever
            chunk_bytes_size: chunk size to iterate over stream downloaded data
            chunk_time_size: split the audio files is chunk with this time
        """
        if self.record_to_time is not None:
            time_now = datetime.now(self.timezone).time()
            while time_now >= self.record_to_time:
                logger.info(f'Now {time_now} is late to save')
                sleep(90)
                time_now = datetime.now(self.timezone).time()

        if self.record_from_time is not None:
            time_now = datetime.now(self.timezone).time()
            while time_now < self.record_from_time:
                logger.info(f'Now {time_now} is early to save')
                sleep(90)
                time_now = datetime.now(self.timezone).time()

        c = 0
        for stream in self.streams:

            c += 1
            url = stream['url']
            logger.info(f'Attempt to record from {url}')
            try:
                r = requests.get(url, stream=True)
            except Exception as e:
                logger.error(f'Error connecting to stream {c} {url}: {e}')
                continue

            extension = stream.get('extension', 'mp3')
            start, stream_path = self.generate_stream_path(extension=extension)
            self.last_start = start
            f = open(stream_path, 'wb')
            logger.info(f'Recording from {url}')
            last_start = start
            c = 0
            for block in r.iter_content(chunk_bytes_size):
                c += 1
                f.write(block)
                logger.debug('  ... chunk saved')

                now = datetime.now(self.timezone)
                elapsed = now - start
                if total_seconds > 0 and elapsed >= timedelta(seconds=total_seconds):
                    logger.info(f'Finish total_seconds recording {now}')
                    break
                elif now - last_start >= timedelta(seconds=chunk_time_size):
                    logger.info(f'{now} Elapsed {elapsed} Finish chunk {c}')
                    self.chunk_finished(stream_path)
                    last_start, stream_path = self.generate_stream_path(extension=extension)
                    self.last_start = last_start
                    f.close()
                    f = open(stream_path, 'wb')
                elif self.record_to_time is not None:
                    time_now = datetime.now(self.timezone).time()
                    if time_now >= self.record_to_time:
                        logger.info(f'Finished day time {self.record_to_time} at {time_now}')
                        break

            f.close()
            # last chunk
            self.chunk_finished(stream_path)
            return stream_path

    def chunk_finished(self, stream_path):
        """ An audio chunk finished. We can post-process and/or upload """
        logger.info('Chunk finished')
        metadata = {
            'stream_name': self.name,
            'short_name': self.short_name,
            'started': self.last_start,
            'finished': datetime.now(self.timezone)
        }
        for ppf in self.post_process_functions:
            fn = ppf['fn']
            logger.info(f'Running {fn}')
            params = ppf.get('params', {})
            stream_path, metadata = fn(stream_path, metadata=metadata, **params)
            logger.info(f'{fn} finished')
