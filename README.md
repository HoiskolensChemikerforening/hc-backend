# chemie
hc.ntnu.no / chemie.no

## Development setup

#### Install requirements
pip install -r requirements.txt

#### Set up database
To create a local database with default settings: 
```shell
python manage_migrations.py
```
#### Load environment variables
Check our secrets in production and paste them into Pycharm.

#### Load fixtures
```shell
python manage.py loaddata fixtures/*.json
```

#### Send mail
If a mail is sent with postoffice, it is queued and not yet sent.
```
python manage.py send_queued_mail 
```

#### Export models to json
```
python manage.py dumpdata --natural-foreign --exclude contenttypes app.model app2.model > my_dump.json
```

## Production environment
Edit the .env file to suit your needs

```
docker-compose up -d --build
```

#### Update production
```
git stash && git pull --rebase && git pop && docker-compose restart
```
