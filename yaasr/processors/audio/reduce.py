import logging
import os
from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError


logger = logging.getLogger(__name__)


def tryopen(stream_path):
    # https://github.com/jiaaro/pydub
    extension = stream_path.split('.')[-1]
    extensions = [extension, 'aac', 'mp4', 'mp3', 'flv', 'ogg', 'wma', 'wav']
    for ext in extensions:
        try:
            audio = AudioSegment.from_file(stream_path, ext)
        except CouldntDecodeError:
            # maybe the codec is not the format
            logger.error
        else:
            logging.info(f'{ext} worked')
            return audio
    raise Exception(f'Pydub can\'t decode {stream_path} from {extensions}')


def reformat(stream_path,
             audio_format='mp3',
             mono=True,
             delete_on_success=False):
    """ change the format and return new format with desired bitrate """
    audio = tryopen(stream_path)
    # if mono:
    #     audio = audio.set_channels(1)
    filename = '.'.join(stream_path.split('.')[:-1])
    new_file_name = f'{filename}.{audio_format}'

    if audio_format == 'mp3':
        parameters = [
            "-ab", "16k",
            "-ar", "8000"
        ]
    elif audio_format == 'ogg':
        parameters = [
            "-ab", "16k",
            "-ar", "8000"
        ]

    if mono:
        parameters += ['-ac', '1']

    audio.export(new_file_name, format=audio_format, parameters=parameters)

    if delete_on_success:
        os.remove(stream_path)
    return new_file_name
