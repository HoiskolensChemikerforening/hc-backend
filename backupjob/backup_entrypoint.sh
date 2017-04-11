#!/bin/bash

printenv > /etc/environment
echo "database:5432:webkom:$PGUSER:$PGPASSWORD" > ~/.pgpass

