#!/bin/bash
# A scipt for resetting the local database
# Drops database and user. Recreates these and loads a dump file.
# Usage: ./resetdb.sh dbuser password dbtitle dumpfile
# E.g.: ./resetdb.sh webkom webkom webkom Wednesday.sql


function wipe {
    # arg1: user
    # arg2: dbtitle
    dropuser $1
    dropdb $2
}

function create {
    # arg1: dbtitle
    psql -c "CREATE DATABASE $1;"
}

function load {
    # arg1: user
    # arg2: dbtitle
    # arg3: sql-backup-file
    pg_restore -U $1 -d $2 $3
}

function create_user {
    # arg1: user
    # arg2: dbtitle
    # arg3: password
    psql -d $2 -c "CREATE ROLE $1;"
	psql -d $2 -c "GRANT ALL PRIVILEGES ON DATABASE $2 TO $1;
                     ALTER ROLE $1 PASSWORD '$3';
                     ALTER ROLE $1 WITH LOGIN;"
    psql -c "ALTER USER $1 CREATEDB;"
}

function yolofix {
    psql -d $DB_TITLE -c "GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO $DB_USER;"
}

if [ $# -eq 4 ]; then
    wipe $1 $3
    create $3
    create_user $1 $2 $3 $4
    load $1 $3 $4
else
    echo "Missing arguement!"
    exit
fi


