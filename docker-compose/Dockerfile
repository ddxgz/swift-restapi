FROM ubuntu:14.04

RUN apt-get update && apt-get install -y \
    python3 \
    python-pip \
    gunicorn 

WORKDIR /restapi

RUN pip install -r requirements.txt
