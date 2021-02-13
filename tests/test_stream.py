import json
import os
import pytest
from yaasr.exceptions import StreamFolderNotFoud, StreamDataFileNotFoud
from yaasr.recorder.stream import YStream


STREAMS_FOLDER = os.path.join(os.path.dirname(__file__), "streams")


class TestYStream:

    def test_fail_stream_folder(self):
        """ Test stream folder exists """
        with pytest.raises(StreamFolderNotFoud):
            YStream('not-existent-stream')

    def test_no_data_file_stream(self):
        """ Test data file exists """
        with pytest.raises(StreamDataFileNotFoud):
            YStream('no-data-file-stream', streams_folder=STREAMS_FOLDER)

    def test_bad_json(self):
        """ Test JSON is valid """
        with pytest.raises(json.decoder.JSONDecodeError):
            YStream('bad-json-stream', streams_folder=STREAMS_FOLDER)

    def test_incomplete_json_stream(self):
        """ Test JSON file include all required fields """
        with pytest.raises(KeyError):
            YStream('incomplete-json-stream', streams_folder=STREAMS_FOLDER)
