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
ys = YStream('radio-universidad-cordoba-argentina')
ys.load()
```
