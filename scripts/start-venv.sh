#!/usr/bin/env bash
set -e

# colors
RED="\e[31m"
GREEN="\e[32m"
BLUE="\e[94m"
ENDCOLOR="\e[0m"

ROOT_DIR=$(git rev-parse --show-toplevel)
VENV_NAME=${1-venv}
VENV_PATH="$ROOT_DIR/$VENV_NAME"
PIP_BIN="$VENV_PATH/bin/pip"

if [[ ! -d $VENV_PATH ]]
    then
        echo
        echo -e "${BLUE}Creating venv...${ENDCOLOR}"
        python3 -m venv $VENV_PATH && \
        echo -e "${GREEN}Done!${ENDCOLOR}" && \

        echo -e "${BLUE}Updating pip, setuptools, wheel...${ENDCOLOR}" && \
        $PIP_BIN install -U pip setuptools wheel > /dev/null && \
        echo -e "${GREEN}Done!${ENDCOLOR}" && \

        echo -e "${BLUE}Installing requirements.txt...${ENDCOLOR}" && \
        $PIP_BIN install -r "$ROOT_DIR/src/requirements.txt" > /dev/null && \
        echo -e "${GREEN}Done!${ENDCOLOR}" && \

        echo -e "${BLUE}Installing dev-requirements.txt...${ENDCOLOR}" && \
        $PIP_BIN install -r "$ROOT_DIR/src/dev-requirements.txt" > /dev/null && \
        echo -e "${GREEN}Done!${ENDCOLOR}" && \

        echo -e "${BLUE}Installing app...${ENDCOLOR}" && \
        $PIP_BIN install -e "$ROOT_DIR/src" > /dev/null && \
        echo -e "${GREEN}Done!${ENDCOLOR}" && \

        echo -e "${BLUE}Activating virtual environment (only if sourced)...${ENDCOLOR}" && \
        . ${VENV_PATH}/bin/activate && \
        echo -e "${GREEN}Done!${ENDCOLOR}" && \
        echo
    else
        echo -e "${RED}A virtual environment called $VENV_NAME already exists!${ENDCOLOR}"
        echo
        exit 0
fi
