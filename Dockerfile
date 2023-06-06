
FROM python:3.9

ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY requirements.txt setup.py ./
RUN pip install --no-cache-dir -r requirements.txt

COPY citroen/ citroen/
RUN pip install --no-cache-dir . && \
    rm -rf setup.py requirements.txt
