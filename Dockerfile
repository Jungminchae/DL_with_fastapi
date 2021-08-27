FROM python:3.8-slim-buster

WORKDIR /usr/src/app

COPY . /usr/src/app/

# install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt