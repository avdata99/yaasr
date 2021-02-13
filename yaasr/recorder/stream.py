import json
import logging
import os
from yaasr import STREAMS_FOLDER
from yaasr.exceptions import StreamFolderNotFoud, StreamDataFileNotFoud


logger = logging.getLogger(__name__)


class YStream:
    """ YAASR stream """

    def __init__(self, stream_name, streams_folder=STREAMS_FOLDER):
        self.name = stream_name
        self.streams_folder = streams_folder
        self.stream_folder = self.get_stream()
        data = self.load()
        self.title = data['title']
        self.web_site = data.get('web', None)
        self.streams = data['streams']

    def get_stream(self):
        """ Get the stream folder """
        stream_folder = os.path.join(self.streams_folder, self.name)
        if not os.path.isdir(stream_folder):
            raise StreamFolderNotFoud(f'Stream not found {stream_folder}')

        return stream_folder

    def load(self):
        """ Load the stream data """
        data_file = os.path.join(self.stream_folder, 'data.json')
        if not os.path.isfile(data_file):
            raise StreamDataFileNotFoud(f'Data file not found {data_file}')

        data = json.load(open(data_file))
        return data
