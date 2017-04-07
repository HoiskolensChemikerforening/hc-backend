#!/bin/bash
printenv > /etc/environment
cd /code/
sleep 10
python manage.py migrate
if [ "$DEBUG" == "False" ]
then
  python manage.py collectstatic --noinput
fi

# Django main uwsgi
exec uwsgi --chdir=./ --module=chemie.wsgi:application --env DJANGO_SETTINGS_MODULE=chemie.settings \
--master --pidfile=/tmp/project-master.pid     --http=0.0.0.0:8000 --processes=5 \
--harakiri=20 --max-requests=5000 --vacuum

# Cronmanager uwsgi
uwsgi --chdir=./ --module=chemie.cron_wsgi:application --env DJANGO_SETTINGS_MODULE=chemie.settings \
--master --pidfile=/tmp/project-master-cron.pid --http=0.0.0.0:8001 --processes=5 \
--harakiri=20 --max-requests=5000 --vacuum