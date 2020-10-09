#!/bin/bash

docker pull aquova/discord.py:1.3.4
DIR=`dirname "$(readlink -f "$0")"`
docker run -v $DIR:/autumn -it aquova/discord.py python3 /autumn/src/main.py
