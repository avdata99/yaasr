import json
import os
import pytest
from yaasr.exceptions import StreamFolderNotFound, StreamDataFileNotFound
from yaasr.recorder.stream import YStream


STREAMS_FOLDER = os.path.join(os.path.dirname(__file__), "streams")


class TestYStream:

    def test_fail_stream_folder(self):
        """ Test stream folder exists """
        ys = YStream('not-existent-stream')
        with pytest.raises(StreamFolderNotFound):
            ys.load()

    def test_no_data_file_stream(self):
        """ Test data file exists """
        ys = YStream('no-data-file-stream', streams_folder=STREAMS_FOLDER)
        with pytest.raises(StreamDataFileNotFound):
            ys.load()

    def test_bad_json(self):
        """ Test JSON is valid """
        ys = YStream('bad-json-stream', streams_folder=STREAMS_FOLDER)
        with pytest.raises(json.decoder.JSONDecodeError):
            ys.load()

    def test_incomplete_json_stream(self):
        """ Test JSON file include all required fields """
        ys = YStream('incomplete-json-stream', streams_folder=STREAMS_FOLDER)
        with pytest.raises(KeyError):
            ys.load()
        assert ys.title == "Stream without streams"

    def test_good_stream(self):
        """ Test well defined stream """
        ys = YStream('good-stream', streams_folder=STREAMS_FOLDER)
        ys.load()
        assert ys.title == "Well defined stream"
        assert ys.streams[0]['url'] == "https://wee.defined.org/stream"
