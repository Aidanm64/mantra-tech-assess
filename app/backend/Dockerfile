FROM python:3.10

RUN pip install --upgrade pip

COPY config /config

COPY requirements.txt .
RUN pip install -r requirements.txt

# RUN git clone https://github.com/Markfryazino/wav2lip-hq.git
# RUN pip install -r wav2lip-hq/requirements.txt

WORKDIR /app

COPY . .

EXPOSE 8080

RUN pip install -e src

ENV PYTHONUNBUFFERED 1
