FROM python:3.6.4
RUN mkdir /chemie

ADD requirements /requirements/
ADD manage.py /
RUN pip install -r /requirements/production.txt

WORKDIR /chemie
CMD ["bash", "/chemie/entrypoint.sh"]
