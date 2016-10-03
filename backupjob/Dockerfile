FROM phusion/baseimage:latest

RUN apt-get update && apt-get install -y wget
RUN echo "deb http://apt.postgresql.org/pub/repos/apt/ trusty-pgdg main" >> /etc/apt/sources.list.d/pgdg.list
RUN wget --quiet -O - \ 
    https://www.postgresql.org/media/keys/ACCC4CF8.asc | \
    apt-key add -
RUN apt-get update && apt-get install -y \
    postgresql-client-9.4 \
    postfix \
    zip

COPY chemie-backup /etc/cron.d/
RUN chmod -R 0644 /etc/cron.d/

COPY daily_backup.sh /daily_backup.sh
RUN chmod +x /daily_backup.sh

COPY weekly_backup.sh /weekly_backup.sh
RUN chmod +x /weekly_backup.sh

COPY backup_entrypoint.sh /etc/service/backup/run
RUN chmod +x /etc/service/backup/run

RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
