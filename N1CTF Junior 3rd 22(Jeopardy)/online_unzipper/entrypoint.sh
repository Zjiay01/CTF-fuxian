#!/bin/sh
set -e

RAND=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | head -c 32)
FLAG_FILE="/flag-$RAND.txt"

if [ -n "$FLAG" ]; then
    echo "$FLAG" > "$FLAG_FILE"
fi

unset FLAG
export FLAG=""

exec "$@"
