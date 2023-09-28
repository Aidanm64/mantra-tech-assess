FROM python:3.8.7

RUN apt-get update
RUN apt-get install ffmpeg -y
RUN pip install --upgrade pip

COPY config /config

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY lib/wav2lip-hq/requirements.txt lib/wav2lip-hq/requirements.txt
RUN pip install -r lib/wav2lip-hq/requirements.txt

WORKDIR /app

COPY . .
RUN pip install -e src
RUN mkdir /temp
ENV PYTHONUNBUFFERED 1
