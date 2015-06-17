FROM ubuntu:14.04

RUN apt-get update && apt-get install -y \
    python3 \
    python3.4-dev \
    python-pip \
    gunicorn 

# for copy requirements.txt to container
COPY . /restapi

WORKDIR /restapi

RUN pip install -r requirements.txt
