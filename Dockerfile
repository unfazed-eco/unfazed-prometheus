FROM python:3.12.3-bullseye


COPY . /unfazed_prometheus
WORKDIR /unfazed_prometheus

RUN pip3 install uv
ENV UV_PROJECT_ENVIRONMENT="/usr/local"