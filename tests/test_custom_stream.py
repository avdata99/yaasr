import pytz
from yaasr.recorder.stream import YStream


def test_custom_stream():
    """ test custom stream """
    ys = YStream(stream_name='my-custom-stream')
    ys.timezone = pytz.timezone('America/Argentina/Catamarca')
    ys.destination_folder = 'tests/chunks'
    ys.title = 'My radio title'
    # list of stream (if first fails the second should be used)
    ys.streams = [
        {'url': 'https://failed-stream.com.br/not-exist-stream.mp3'},
        {'url': 'https://avdata99.github.io/yaasr/audios/84-sec-test-radio.mp3'}
    ]
    ys.short_name = 'my-radio'

    ys.record(total_seconds=120, chunk_bytes_size=1, chunk_time_size=5)

    # this is not a real time stream. The download is faster
    assert len(ys.saved_chunks) > 0
