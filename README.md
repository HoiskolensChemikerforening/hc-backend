# chemie
chemie.no

# Install requirements
pip install -r requirements.txt

# Database
python manage.py makemigrations
python manage.py migrate

# Default user
python manage.py createsuperuser

# Send mail
If a mail is sent with postoffice, it is queued and not yet sent.
python manage.py send_queued_mail 

