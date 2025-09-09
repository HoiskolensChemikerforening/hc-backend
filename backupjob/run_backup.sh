#! /bin/bash
# Daily/Weekly/Monthly/Manual backup
# REMOTE_HOST
# REMOTE_SSH_USER 
# REMOTE_BACKUP_DIR 
BACKUP_TYPE="$1"

case $BACKUP_TYPE in
daily)
    echo "Daily"
   BACKUP_DIR="daily"
   TIME_PREFIX=$(date +%A)
    ;;
weekly)
    echo "Weekly"
   BACKUP_DIR="weekly"
   TIME_PREFIX=$((($(date +%-d)-1)/7+1))
    ;;
monthly)
    echo "Monthly"
    BACKUP_DIR="monthly"
    if (( $(date +%-m) % 2)); then
        TIME_PREFIX="odd"
    else 
        TIME_PREFIX="even"
    fi
   #TIME_PREFIX=$(date +%m)
    ;;
*)
    echo -n "Now"
   BACKUP_DIR="manual"
   TIME_PREFIX=$(date +%Y-%m-%d_time_%H%M)
    ;;
esac

cd /code/
if [ "$BACKUP" == "True" ]
then
    NOW=$(date +\%a)
    mkdir /tmp/backup/$NOW -p
    cd /tmp/backup
    /usr/bin/pg_dump -h database -U $PGUSER -Fc $POSTGRES_DB > $NOW/backup.gz 2>> /var/log/syslog
    DBFILE=$REMOTE_BACKUP_DIR/database/$BACKUP_DIR/$TIME_PREFIX.gz
    MD5=($(md5sum $NOW/backup.gz))
    scp -P $REMOTE_PORT -r -o StrictHostKeyChecking=no -i /ssh/backup_key $NOW/backup.gz $REMOTE_SSH_USER@$REMOTE_HOST:$DBFILE
    MD5_SERVER=$(ssh $REMOTE_SSH_USER@$REMOTE_HOST -p $REMOTE_PORT -i /ssh/backup_key -o StrictHostKeyChecking=no DBFILE=$DBFILE 'md5=($(md5sum $DBFILE)); echo $md5')
    rm -r $NOW
    REMOTE_PATH=$REMOTE_BACKUP_DIR/media/$BACKUP_DIR/$TIME_PREFIX
    rsync -vzrltoD -e "ssh -i /ssh/backup_key -p $REMOTE_PORT" --rsync-path="mkdir -p $REMOTE_PATH && rsync" --delete /code/media/ $REMOTE_SSH_USER@$REMOTE_HOST:$REMOTE_PATH --port $REMOTE_PORT

    if [ "$MD5" == "$MD5_SERVER" ]
    then
        echo "$(date +'%m.%d.%Y %H:%M') $BACKUP_DIR backup succeded" >> /var/log/backup.log
    else
        echo "$(date +'%m.%d.%Y %H:%M') $BACKUP_DIR backup FAILED: MD5 MISMATCH" >> /var/log/backup.log
    fi
else
    echo "$(date +'%m.%d.%Y') Backup disabled" >> /var/log/backup.log
fi
