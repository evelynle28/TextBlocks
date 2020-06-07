#!/bin/bash

pipenv shell
nohup python3 server.py > server.log 2>&1 &

echo "PID :: $!" 
