#!/bin/bash

PYTHON=$(which python)
if [ $? -gt 0 ]; then
	echo "No se encuentra 'python' en el PATH, esta instalado?"
	exit 1
fi

echo "Lanzando AOC"
$PYTHON AOC.py