#!/bin/sh
set -e

echo "$FLAG" > /app/flag.txt

unset FLAG

exec python /app/server.py
