FROM python:3.6.4
RUN apt-get update
RUN mkdir /code
ADD requirements.txt /src/
RUN pip install -r /src/requirements.txt

WORKDIR /code
CMD ["bash", "/code/entrypoint.sh"]
