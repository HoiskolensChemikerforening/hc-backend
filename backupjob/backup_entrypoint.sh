#!/bin/bash

printenv > /etc/environment
echo "database:5432:webkom:$PGUSER:$PGPASSWORD" >> ~/.pgpass
chmod 0600 ~/.pgpass
