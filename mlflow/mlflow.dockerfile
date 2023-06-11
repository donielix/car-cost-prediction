FROM ghcr.io/mlflow/mlflow

ENV POSTGRES_USER $POSTGRES_USER
ENV POSTGRES_PASSWORD $POSTGRES_PASSWORD
ENV POSTGRES_DB $POSTGRES_DB
ENV PGPORT $PGPORT
ENV PGHOST $PGHOST

RUN apt update && \
    apt install libpq-dev -y && \
    apt install gcc -y && \
    pip install -U pip setuptools wheel && \
    pip install psycopg2

# Create a new user
RUN useradd -ms /bin/bash mlflow

WORKDIR /home/mlflow

# Switch to the new user
USER mlflow

RUN mkdir artifacts

CMD mlflow server --backend-store-uri \
    postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${PGHOST}:${PGPORT}/${POSTGRES_DB} \
    --artifacts-destination file:///home/mlflow/artifacts --host 0.0.0.0 --port 5000 \
    --serve-artifacts
