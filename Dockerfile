# syntax=docker/dockerfile:1
FROM python:3.11
COPY . .
RUN pip install -r requirements.txt
