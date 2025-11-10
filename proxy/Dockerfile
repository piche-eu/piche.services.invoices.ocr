FROM python:3.12.1-slim-bullseye
# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /usr/app
COPY . /usr/app
RUN apt-get update
RUN apt-get install python python3-pip -y
RUN apt install build-essential python3-dev
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libjpeg-dev \
    && rm -rf /var/lib/apt/lists/*
RUN apt install zlib1g
COPY ./requirements.txt requirements.txt
RUN python3 -m pip install --upgrade pip

RUN python3 -m pip install  -r requirements.txt
RUN pip3 install Cython
RUN pip3 install fastapi[standart]
RUN pip3 install --upgrade Cython
RUN python3 -m pip install --upgrade Pillow
RUN pip3 install -r requirements.txt
RUN pip3 install grpcio==1.76.0
RUN pip3 install protobuf==6.33.0
RUN pip3 install pymupdf
RUN pip3 install ollama

EXPOSE 8000
