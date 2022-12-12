#!/bin/sh

set -o errexit
set -o nounset

echo "start"

python manage.py migrate --noinput
nosetests ./tests
