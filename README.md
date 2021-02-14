![Build status](https://github.com/avdata99/yaasr/workflows/Build/badge.svg?branch=main)
[![Pypi py version](https://img.shields.io/pypi/pyversions/yaasr)](https://pypi.org/project/yaasr/)
[![GitHub All Releases](https://img.shields.io/github/downloads/avdata99/yaasr/total)](https://github.com/avdata99/yaasr/releases)
[![GitHub Issues](https://img.shields.io/github/issues/avdata99/yaasr)](https://github.com/avdata99/yaasr/issues)
[![GitHub PR](https://img.shields.io/github/issues-pr/avdata99/yaasr)](https://github.com/avdata99/yaasr/pulls)
[![Licence](https://img.shields.io/github/license/avdata99/yaasr)](https://github.com/avdata99/yaasr/blob/main/LICENSE)
[![Last Commit](https://img.shields.io/github/last-commit/avdata99/yaasr)](https://github.com/avdata99/yaasr/commits/main)

# Yet Another Audio Stream Recorder

Audio stream recorded and static DB for radio stations

## Usage

Install
```
pip install yaasr
```

Load a pre-defined stream

```python
from yaasr.recorder.stream import YStream
from yaasr.processors.audio.reduce import reformat
from yaasr.processors.archive.ssh import upload_ssh


logging.config.fileConfig('yaasr/log.conf')
logging.info('Started')

ys = YStream('radio-universidad-cordoba-argentina')
ys.load()

# post-processors (you can combine or create new processors)
ys.post_process_functions = [
    {
        'fn': reformat,
        'params': {
            'audio_format': 'mp3',
            'bitrate': '16k',
            'delete_on_success': True
        }
    },
    {
        'fn': upload_ssh,
        'params': {
            'host': 'myhost.com',
            'user': 'username',
            'password': 'mypass',
            'destination_folder': '/home/username/audios/',
            'port': 901,
            'delete_on_success': True
        }
    }
]
ys.record(total_seconds=300, chunk_bytes_size=1024, chunk_time_size=60)

logging.info('Finished')

```

Results

```
2021-02-14 13:06:36,876 - root - INFO - Started
2021-02-14 13:07:41,158 - root - INFO - aac worked
2021-02-14 13:07:42,479 - root - INFO - Uploading stream-radio-universidad-cordoba-argentina-20210214130638-16k.mp3
2021-02-14 13:07:42,897 - paramiko.transport - INFO - Connected (version 2.0, client OpenSSH_7.4)
2021-02-14 13:07:44,820 - paramiko.transport - INFO - Authentication (password) successful!
2021-02-14 13:07:45,976 - root - INFO - Copying stream-radio-universidad-cordoba-argentina-20210214130638-16k.mp3
2021-02-14 13:07:48,017 - root - INFO - Deleting radio-universidad-cordoba-argentina/stream-radio-universidad-cordoba-argentina-20210214130638-16k.mp3
2021-02-14 13:08:49,742 - root - INFO - aac worked
2021-02-14 13:08:50,703 - root - INFO - Uploading radio-universidad-cordoba-argentina/stream-radio-universidad-cordoba-argentina-20210214130748-16k.mp3
2021-02-14 13:08:51,050 - paramiko.transport - INFO - Connected (version 2.0, client OpenSSH_7.4)
2021-02-14 13:08:52,731 - paramiko.transport - INFO - Authentication (password) successful!
2021-02-14 13:08:53,550 - root - INFO - Copying radio-universidad-cordoba-argentina/stream-radio-universidad-cordoba-argentina-20210214130748-16k.mp3
2021-02-14 13:08:54,985 - root - INFO - Deleting radio-universidad-cordoba-argentina/stream-radio-universidad-cordoba-argentina-20210214130748-16k.mp3
2021-02-14 13:09:57,814 - root - INFO - aac worked
2021-02-14 13:09:58,843 - root - INFO - Uploading radio-universidad-cordoba-argentina/stream-radio-universidad-cordoba-argentina-20210214130854-16k.mp3
2021-02-14 13:09:59,389 - paramiko.transport - INFO - Connected (version 2.0, client OpenSSH_7.4)
2021-02-14 13:10:01,370 - paramiko.transport - INFO - Authentication (password) successful!
2021-02-14 13:10:02,257 - root - INFO - Copying from radio-universidad-cordoba-argentina/stream-radio-universidad-cordoba-argentina-20210214130854-16k.mp3
2021-02-14 13:10:03,590 - root - INFO - Deleting radio-universidad-cordoba-argentina/stream-radio-universidad-cordoba-argentina-20210214130854-16k.mp3
2021-02-14 13:11:05,828 - root - INFO - aac worked
2021-02-14 13:11:06,793 - root - INFO - Uploading radio-universidad-cordoba-argentina/stream-radio-universidad-cordoba-argentina-20210214131003-16k.mp3
2021-02-14 13:11:07,176 - paramiko.transport - INFO - Connected (version 2.0, client OpenSSH_7.4)
2021-02-14 13:11:09,242 - paramiko.transport - INFO - Authentication (password) successful!
2021-02-14 13:11:10,146 - root - INFO - Copying from radio-universidad-cordoba-argentina/stream-radio-universidad-cordoba-argentina-20210214131003-16k.mp3
2021-02-14 13:11:11,991 - root - INFO - Deleting radio-universidad-cordoba-argentina/stream-radio-universidad-cordoba-argentina-20210214131003-16k.mp3
2021-02-14 13:11:38,845 - root - INFO - aac worked
2021-02-14 13:11:39,369 - root - INFO - Uploading radio-universidad-cordoba-argentina/stream-radio-universidad-cordoba-argentina-20210214131111-16k.mp3
2021-02-14 13:11:39,840 - paramiko.transport - INFO - Connected (version 2.0, client OpenSSH_7.4)
2021-02-14 13:11:41,629 - paramiko.transport - INFO - Authentication (password) successful!
2021-02-14 13:11:42,404 - root - INFO - Copying radio-universidad-cordoba-argentina/stream-radio-universidad-cordoba-argentina-20210214131111-16k.mp3
2021-02-14 13:11:43,598 - root - INFO - Deleting radio-universidad-cordoba-argentina/stream-radio-universidad-cordoba-argentina-20210214131111-16k.mp3
2021-02-14 13:11:43,599 - root - INFO - Finished
```

![ssh files](docs/img/sshed.png)
