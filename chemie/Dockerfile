FROM python:3.5.1
RUN apt-get update
RUN mkdir /code
ADD requirements.txt /src/
RUN pip install -r /src/requirements.txt
#ADD . /code/
WORKDIR /code
CMD ["bash", "/code/entrypoint.sh"]
