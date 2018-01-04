FROM python:3.6-alpine

RUN mkdir -p /code/data
ADD lib /code/lib
ADD requirements.txt /code/requirements.txt
ADD diff_runner.py /code/diff_runner.py

WORKDIR code

RUN pip install -r requirements.txt