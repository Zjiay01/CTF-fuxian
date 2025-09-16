#!/bin/sh

if [ "$FLAG" ]; then
  echo "$FLAG" > /flag
  unset FLAG
fi

python app.py