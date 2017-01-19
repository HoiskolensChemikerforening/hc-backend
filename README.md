# chemie
chemie.no

# Install requirements
pip install -r requirements.txt

# Database
python manage_migrations.py

# Default user
Made through python manage_migrations.py above. Run only once

# Send mail
If a mail is sent with postoffice, it is queued and not yet sent.
python manage.py send_queued_mail 

