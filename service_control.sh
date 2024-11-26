#!/bin/bash

HOME_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
APP_NAME="wsgi"
GUNICORN_CONFIG="${HOME_PATH}/service_config.py"

start() {
    echo "Starting Gunicorn..."
    if [ -d "${HOME_PATH}/logs" ]
    then
        echo "logs start"
    else
        mkdir "${HOME_PATH}/logs"
        echo "logs directory created..."
    fi
    sudo "${HOME_PATH}/venv/bin/gunicorn" -c ${GUNICORN_CONFIG} ${APP_NAME}:app
}

stop() {
    echo "Stopping Gunicorn..."
    sudo kill -INT $(ps -eo pid,command | grep "${HOME_PATH}/venv/bin/gunicorn" | grep -v grep | awk '{print $1}')
}

restart() {
    echo $0
    bash $0 stop
    echo "……"
    sleep 5
    bash $0 start
}


case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        restart
        ;;
    *)
        echo "Usage: $0 {start|stop|restart}"
        exit 1
esac

exit 0
