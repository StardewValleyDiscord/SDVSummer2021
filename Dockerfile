FROM python:alpine

RUN apk update && apk add \
    gcc \
    musl-dev

ADD requirements.txt /autumn/requirements.txt
RUN pip3 install -r /autumn/requirements.txt
