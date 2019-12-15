#!/bin/bash

python3 src/encode.py frames/VLC
python3 cat2video.py frames/VLC frames/VLC.avi
python3 "src/05.decode.video.py" frames/VLC
