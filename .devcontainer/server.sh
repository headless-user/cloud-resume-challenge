#! /bin/bash

nginx
nohup fastapi run backend/main.py >/tmp/fastapi.log 2>&1 &
