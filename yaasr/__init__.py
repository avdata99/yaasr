import os


__VERSION__ = '0.4.9'
BASE_FOLDER = os.path.dirname(__file__)
STREAMS_FOLDER = os.path.join(BASE_FOLDER, "streams")


def get_all_streams():
    streams = []
    for subdir, dirs, files in os.walk(STREAMS_FOLDER):
        for sdir in dirs:
            data_file = os.path.join(STREAMS_FOLDER, sdir, 'data.json')
            if os.path.isfile(data_file):
                streams.append(sdir)

    return streams
