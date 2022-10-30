# chemie
hc.ntnu.no

## Development setup

#### Install requirements
Install PostgreSQL for your OS.

Create a virtual environment with Python 3.6+. Note that the project is incompatible with Python 3.10+.

Run the following to install requirements for the project.
```shell
pip install -r requirements/development.txt
```
On newer Mac architectures, you might have to run the following in your terminal before installing the project dependencies: 
```shell
export LDFLAGS="-L/opt/homebrew/opt/openssl@1.1/lib $LDFLAGS"
```
Note that the path to `openssl/lib` might vary depending on how it's been installed.

#### Set up database
Create a local database with default settings. Update settings
file with database credentials if needed.
```shell
python manage_migrations.py
```

#### Load fixtures
Flatpages and email templates are stored in the fixtures folder. 
Load these:
```shell
python manage.py loaddata fixtures/*.json
```

#### Send mail (optional)
Postoffice is the mail backend in this project. All emails are queued
 and not sent until you run this command:
```shell
python manage.py send_queued_mail
```
The following environment variables must be set and you must be on 
eduroam or use VPN to NTNU.
```shell
EMAIL_HOST_USER=webkom@hc.ntnu.no
EMAIL_HOST=smtp.ansatt.ntnu.no
```

#### Re-create email templates
Email templates are twofold: A HTML template and a simple text 
template with no styling. These must be loaded into the database 
before use. This is done by running:

```shell
python manage.py import_emails
 ```
This requires  [MJML](https://mjml.io) to be installed.
Warning: There is an issue with the import_emails program which leads to all of the templates being deleted without any new ones being created to replace them.
Make sure to fix this and test it locally before attempting to use this program.
 
### DevOps
#### Export models to json
```shell
python manage.py dumpdata --natural-foreign --exclude contenttypes app.model app2.model > my_dump.json
```

## Production environment
Edit the `.env` file to suit your needs

```
docker-compose up -d --build
```

#### Update production
```
git stash && git pull --rebase && git pop && docker-compose restart
```
Run this in the terminal
```
export DOCKER_BUILDKIT=1
export COMPOSE_DOCKER_CLI_BUILD=1
```

## Add packages to requirements
We use pip-tools to make our requirement files easy to understand. To 
add a new package to the project you need to update either of the files 
`requirements/base.in`, `requirements/development.in` or 
`requirements/production.in` with the package and then run the line below 
to update the files `requirements/base.txt`, `requirements/development.txt` 
and `requirements/production.txt` that is used when setting up the project.
```shell
pip-compile requirements/base.in > requirements/base.txt
pip-compile requirements/development.in > requirements/development.txt
pip-compile requirements/production.in > requirements/production.txt
```
