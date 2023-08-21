FROM python:3.10
RUN apt-get update -y
RUN apt-get upgrade -y

WORKDIR /app

COPY ./requirements.txt ./
COPY ./.env ./
RUN pip install -r requirements.txt
COPY ./skyeng ./