#!/usr/bin/env bash
set -e

ROOT_DIR=$(git rev-parse --show-toplevel)

if ! command -v docker-compose &> /dev/null
then
    COMPOSE_COMMAND="docker compose"
else
    COMPOSE_COMMAND="docker-compose"
fi


$COMPOSE_COMMAND -f "$ROOT_DIR/db/docker-compose.yml" build > /dev/null
$COMPOSE_COMMAND -f "$ROOT_DIR/db/docker-compose.yml" up -d
