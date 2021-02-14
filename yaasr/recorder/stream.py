import json
import logging
import os
import requests
from datetime import datetime, timedelta
from yaasr import STREAMS_FOLDER
from yaasr.exceptions import StreamFolderNotFoud, StreamDataFileNotFoud


logger = logging.getLogger(__name__)


class YStream:
    """ YAASR stream """

    def __init__(self, stream_name, streams_folder=STREAMS_FOLDER):
        self.name = stream_name
        self.streams_folder = streams_folder

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

        data = json.load(open(data_file))

        self.title = data['title']
        self.web_site = data.get('web', None)
        self.streams = data['streams']

    def record(self, seconds=10):
        """ Record the online stream """
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
            stream_path = os.path.join(self.stream_folder, f'stream.{extension}')
            start = datetime.now()
            f = open(stream_path, 'wb')
            logger.info(f'Recording from {url}')
            for block in r.iter_content(1024):
                logger.debug('  ... chunk saved')
                if datetime.now() - start >= timedelta(seconds=seconds):
                    logger.info('Finish recording')
                    break
                f.write(block)
            self.stream_path = stream_path
            return stream_path
