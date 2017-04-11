FROM phusion/baseimage:latest

RUN apt-get update && apt-get install -y wget
RUN echo "deb http://apt.postgresql.org/pub/repos/apt/ trusty-pgdg main" >> /etc/apt/sources.list.d/pgdg.list
RUN wget --quiet -O - \ 
    https://www.postgresql.org/media/keys/ACCC4CF8.asc | \
    apt-key add -
RUN apt-get update && apt-get install -y \
    postgresql-client-9.6 \
    postfix \
    zip \
    rsync

RUN mkdir /ssh
COPY ssh_key /ssh/key

COPY backup-cron /etc/cron.d/
RUN chmod -R 0644 /etc/cron.d/

COPY run_backup.sh /run_backup.sh
RUN chmod +x /run_backup.sh

COPY backup_entrypoint.sh /etc/service/backup/run
RUN chmod +x /etc/service/backup/run

RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
