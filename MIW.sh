#!/bin/bash

PYTHON=$(which python)
if [ $? -gt 0 ]; then
	echo "No se encuentra 'python' en el PATH, esta instalado?"
	exit 1
fi

DJANGO=$($PYTHON -c "import django")
if [ $? -gt 0 ]; then
	echo "No se encuentra 'django', esta instalado?"
	exit 1
fi

export LANG="es_ES.UTF-8"
export LC_COLLATE="es_ES.UTF-8"
export LC_CTYPE="es_ES.UTF-8"
export LC_MESSAGES="es_ES.UTF-8"
export LC_MONETARY="es_ES.UTF-8"
export LC_NUMERIC="es_ES.UTF-8"
export LC_TIME="es_ES.UTF-8"
export LC_ALL=

HOST=$1
PORT=$2

cd MIW/
$PYTHON manage.py runserver $HOST:$PORT