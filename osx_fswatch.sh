#!/bin/bash
DIR="$(cd "$(dirname "$0")" && pwd)"
if [ ! -d "$1" ]; then
  echo "First parameter needs to be a valid relative or absolute path."
  exit
fi

if [ ! -f "$2" ]; then
  echo "Second parameter needs to be valid executable."
  exit
fi

SYNC_PATH=$(cd "$(dirname "$1")"; pwd)

head=$(dirname "$1")
head=$(cd "$head" && pwd)
SYNC_PATH="$head/$(basename $1)"

head=$(dirname "$2")
head=$(cd "$head" && pwd)
SCRIPT_PATH="$head/$(basename $2)"
LOG_PATH="${SYNC_PATH}/fswatch.log"
touch $LOG_PATH

echo "Running script located at: ${SCRIPT_PATH}"
echo "On file change in folder: ${SYNC_PATH}"
echo "Writing log output to : ${LOG_PATH}"
exec $SCRIPT_PATH

# brew install fswatch

fswatch -o $SYNC_PATH | xargs -n1 $SCRIPT_PATH | tee $LOG_PATH
