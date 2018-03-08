FROM python:3.6.4
RUN mkdir /chemie

ADD requirements /requirements/
ADD manage.py /
RUN pip install -r /requirements/requirements.txt
RUN pip install -r /requirements/prod.txt

WORKDIR /chemie
CMD ["bash", "/code/entrypoint.sh"]
