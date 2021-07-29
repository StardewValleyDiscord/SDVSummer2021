FROM python:alpine

RUN apk update && apk add \
    build-base \
    git \
    sqlite

COPY requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt

CMD ["python3", "-u", "/summer/main.py"]
