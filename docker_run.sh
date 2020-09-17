#!/bin/bash

DIR=`dirname "$(readlink -f "$0")"`
docker build -t aquova/autumn $DIR
# Load this directory in container filespace as /autumn and run main
docker run -v $DIR:/autumn -it aquova/autumn python3 /autumn/src/main.py
