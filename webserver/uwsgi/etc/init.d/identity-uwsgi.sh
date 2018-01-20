#!/bin/bash
USER="django"
PIDFILE="/home/django/identity/identity-uwsgi.pid"

function start(){
  if ! ps -p `cat ${PIDFILE}` > /dev/null;
  then
    su - ${USER} /bin/sh -c "source /home/django/env/bin/activate && exec uwsgi --pidfile=${PIDFILE} --master --ini /etc/init.d/identity-uwsgi.ini"
  else
    echo 'identity uwsgi is already running'
  fi  
}

function stop(){
    kill -9 `cat ${PIDFILE}`
}

$1