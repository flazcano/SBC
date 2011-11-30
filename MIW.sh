#!/bin/bash

PYTHON=`which python`
if [ $? -gt 0 ]; then
	echo "No se encuentra 'python' en el PATH, esta instalado?"
	exit 1
fi

HOST=$1
PORT=$2

cd MIW/
$PYTHON manage.py runserver $HOST $PORT