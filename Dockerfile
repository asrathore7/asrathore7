# Base Image
FROM python:3.8

# create and set working directory
RUN mkdir /app
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .

ADD . /app/

ENV PYTHONUNBUFFERED 1

RUN pip3 install --upgrade pip
