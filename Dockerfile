# syntax = docker/dockerfile:experimental
FROM python:3.7
RUN mkdir /chemie
RUN apt update && apt install -y netcat

ADD requirements /requirements/
ADD emails /emails/
ADD manage.py /
# This line along with the first one caches pip
# packages. It is experimental and might break.
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r /requirements/production.txt

WORKDIR /chemie
CMD ["bash", "/chemie/entrypoint.sh"]
