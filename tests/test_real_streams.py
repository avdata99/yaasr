from yaasr import get_all_streams
from yaasr.recorder.stream import YStream


def test_all_streams():
    streams = get_all_streams()

    unique_names = []
    for stream in streams:
        ys = YStream(stream)
        ys.load()
        # it works ys.record(total_seconds=30, chunk_bytes_size=512, chunk_time_size=10)
        if ys.short_name in unique_names:
            raise Exception(f'Duplicated stream name {ys.short_name}')
        unique_names.append(ys.short_name)
