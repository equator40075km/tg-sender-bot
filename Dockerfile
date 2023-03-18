FROM python:3.8

RUN mkdir /app-bot
WORKDIR /app-bot

COPY . .

RUN python3.8 -m pip install -r requirements.txt