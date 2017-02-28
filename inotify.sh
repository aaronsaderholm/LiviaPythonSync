#!/bin/bash

BASEDIR=$(dirname "$0")
cd $BASEDIR


while inotifywait -r -e modify,move,create,delete $BASEDIR; do
	echo "The file '$file' appeared in directory '$path' via '$action'"
    python3 main.py -c ../content/config.json -o download
done
