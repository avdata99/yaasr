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


def reformat(stream_path, audio_format='mp3', bitrate='16k', delete_on_success=False):
    """ change the format and return new format with desired bitrate """
    audio = tryopen(stream_path)
    filename = ''.join(stream_path.split('.')[:-1])
    new_file_name = f'{filename}-{bitrate}.{audio_format}'
    audio.export(new_file_name, format=audio_format, bitrate=bitrate)

    if delete_on_success:
        os.remove(stream_path)
    return new_file_name
