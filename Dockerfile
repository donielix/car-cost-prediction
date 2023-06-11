
FROM python:3.10

ENV PYTHONUNBUFFERED=1
ARG POETRY=1.5.1

WORKDIR /code

RUN pip install -U pip setuptools wheel && \
    pip install poetry==${POETRY}

COPY poetry.lock pyproject.toml README.md ./
COPY src/ ./src/

RUN poetry install --no-dev
ENTRYPOINT [ "poetry", "run", "src/models/exponential/train.py" ]
