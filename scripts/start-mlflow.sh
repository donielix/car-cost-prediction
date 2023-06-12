#!/usr/bin/env bash
# Starts a local MLFlow server, with remote storage for artifacts on S3
# An instance of PostgreSQL must be running on port 5432
set -e

ROOT_DIR=$(git rev-parse --show-toplevel)

if ! command -v docker-compose &> /dev/null
then
    COMPOSE_COMMAND="docker compose"
else
    COMPOSE_COMMAND="docker-compose"
fi

cd "${ROOT_DIR}/mlflow"

$COMPOSE_COMMAND -f "docker-compose.yml" build > /dev/null
$COMPOSE_COMMAND -f "docker-compose.yml" up -d
