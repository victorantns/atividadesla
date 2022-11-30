#!/bin/sh

set -e

pip install --upgrade pip

pip install -r requirements.txt

python init_db.py

exec "$@"