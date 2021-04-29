import json
import logging
import os
import pytz
import requests
from datetime import datetime, timedelta
from yaasr import STREAMS_FOLDER, __VERSION__
from yaasr.exceptions import StreamFolderNotFound, StreamDataFileNotFound


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

        # chunks saved
        self.saved_chunks = []

        # Notify events to an external URL
        self.notify_url = None

    def set_notifications(self, url, headers={}, params={}):
        self.notify_url = url
        self.notify_extra_params = params
        self.notify_headers = headers

    def get_stream_folder(self):
        """ Get the stream folder """
        stream_folder = os.path.join(self.streams_folder, self.name)
        if not os.path.isdir(stream_folder):
            raise StreamFolderNotFound(f'Stream not found {stream_folder}')

        return stream_folder

    def load(self):
        """ Load and validate the stream data """
        self.stream_folder = self.get_stream_folder()
        data_file = os.path.join(self.stream_folder, 'data.json')
        if not os.path.isfile(data_file):
            raise StreamDataFileNotFound(f'Data file not found {data_file}')

        self.data = json.load(open(data_file))

        self.title = self.data['title']
        self.web_site = self.data.get('web', None)
        self.streams = self.data['streams']
        self.short_name = self.data.get('short_name', self.name)
        self.timezone = pytz.timezone(self.data.get('timezone', 'UTC'))

    def generate_stream_path(self, extension):
        now = datetime.now(self.timezone)
        stime = now.strftime(self.str_chunk_time_format)
        if not os.path.isdir(self.destination_folder):
            default_folder = '~'
            logger.error(f'Destination folder doesn\'t exists {self.destination_folder}. Using {default_folder}')
            self.destination_folder = default_folder
        stream_path = os.path.join(self.destination_folder, f'{self.short_name}-{stime}.{extension}')
        return now, stream_path

    def record(self, total_seconds=0, chunk_bytes_size=1024, chunk_time_size=60):
        """ Record the online stream

        Params:
            total_seconds: total time to save from the stream. 0 is for ever
            chunk_bytes_size: chunk size to iterate over stream downloaded data
            chunk_time_size: split the audio files is chunk with this time
        """

        c = 0
        # try all streams
        for stream in self.streams:

            c += 1
            url = stream['url']
            logger.info(f'Attempt to record from {url}')
            try:
                r = requests.get(url, stream=True)
            except Exception as e:
                error = f'Error connecting to stream {c} {url}: {e}'
                logger.error(error)
                self.notify('START_RECORDING', data={'url': url}, error=error)
                continue

            self.notify('START_RECORDING', {'url': url})
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

            f.close()
            # last chunk
            self.chunk_finished(stream_path)
            self.notify('FINISH_RECORDING', {'url': url})
            return stream_path

    def chunk_finished(self, stream_path):
        """ An audio chunk finished. We can post-process and/or upload """
        logger.info('Chunk finished')
        metadata = {
            'stream_name': self.name,
            'short_name': self.short_name,
            'started': self.last_start,
            'finished': datetime.now(self.timezone),
            'extension': stream_path.split('.')[-1]
        }
        self.saved_chunks.append(metadata)

        ppfs = []
        order = 0
        for ppf in self.post_process_functions:
            order += 1
            start_time = datetime.now(self.timezone)
            fn = ppf['fn']
            logger.info(f'Running {fn}')
            params = ppf.get('params', {})
            try:
                stream_path, metadata = fn(stream_path, metadata=metadata, **params)
            except Exception as e:
                error = f'Error at postprocess function {e}'
                self.notify('CHUNK_FINISHED', error=error)
                raise
            logger.info(f'{fn} finished')
            elapsed = datetime.now(self.timezone) - start_time
            ppfs.append({
                'order': order,
                'function': fn.__name__,
                'elapsed': str(elapsed),
                # TODO ensure pickle this 'params': params,
                # TODO ensure pickle this  'metadata': metadata
            })
        data = {
            'chunk_started': self.last_start.strftime(self.str_chunk_time_format)
        }

        data.update({'post_process_functions': ppfs})
        self.notify('CHUNK_FINISHED', data)
        logger.info('Chunk finished: finished (?) and notified')

    def notify(self, event_name, data={}, error=None):
        """ notify status to an external URL """
        if self.notify_url is None:
            return
        url = self.notify_url
        data['extras'] = self.notify_extra_params

        # default params
        data['event'] = event_name
        data['stream_name'] = self.name
        data['yaasr_version'] = __VERSION__
        data['error'] = error

        # TODO we can't POST a nested DICTs (e.g. post_process_functions)
        for key, value in data.items():
            if type(value) in [list, dict]:
                data[key] = json.dumps(value)

        headers = {'User-Agent': f'YAASR v{__VERSION__}'}
        # Use secure tokens from your server to avoid assholes.
        headers.update(self.notify_headers)
        try:
            requests.post(url=url, headers=headers, data=data)
        except Exception as e:
            logger.error(f'Error notifying: {e}')
