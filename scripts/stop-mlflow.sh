#!/usr/bin/env bash

set -e

ROOT_DIR=$(git rev-parse --show-toplevel)

if ! command -v docker-compose &> /dev/null
then
    COMPOSE_COMMAND="docker compose"
else
    COMPOSE_COMMAND="docker-compose"
fi

cd "${ROOT_DIR}/mlflow"

$COMPOSE_COMMAND -f "docker-compose.yml" down "$@"
