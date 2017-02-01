"""
Description: Create migrations for all apps and migrate them
@Author: Sindre Bakke Øyen
Date (started): 18.01.2017
"""
import os
from django.conf import settings
from django.utils.module_loading import import_module
from django.core.management import execute_from_command_line
os.environ['DJANGO_SETTINGS_MODULE'] = 'chemie.settings'


def initial_migrations():
    execute_from_command_line(["manage.py", "migrate"])
    apps = []
    for appname in settings.INSTALLED_APPS:
        apps.append(import_module(appname))
        try:
            execute_from_command_line(["manage.py", "makemigrations", appname])
            execute_from_command_line(["manage.py", "migrate", appname])
        except:
            continue
        execute_from_command_line(["manage.py", "makemigrations", "thumbnail"])
        execute_from_command_line(["manage.py", "migrate", "thumbnail"])
    #print("\n\nNow creating admin user. Please follow instructions below (you can press enter to skip email when prompted)")
    #execute_from_command_line(["manage.py", "createsuperuser"])


if __name__ == '__main__':
    initial_migrations()