#!/bin/sh

python app.py &
nginx -g 'daemon off;'