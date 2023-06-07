#!/usr/bin/env bash
# Stop docker database service, optionally removing mounted volumes
set -e

ROOT_DIR=$(git rev-parse --show-toplevel)

usage() {                                 # Function: Print a help message.
  echo "Usage: $0 [ -v ]" 1>&2
  echo "    -v  Removes mounted volumes after stopping db." 1>&2
}
exit_abnormal() {                         # Function: Exit with error.
  usage
  exit 1
}

if ! command -v docker-compose &> /dev/null
then
    COMPOSE_COMMAND="docker compose"
else
    COMPOSE_COMMAND="docker-compose"
fi

while getopts vh OPT
do
    case "$OPT" in
        v) v=1 ;;
        h)
            usage
            exit 0
            ;;
        *) exit_abnormal ;;
    esac
done

if [ -z "$v" ]; then
    $COMPOSE_COMMAND -f "$ROOT_DIR/db/docker-compose.yml" down
else
    echo "Removing volumes..."
    $COMPOSE_COMMAND -f "$ROOT_DIR/db/docker-compose.yml" down -v
fi
