#!/usr/bin/env bash

PATH=/usr/local/bin:$PATH
cd /home/steyn/su-marks/
pipenv install
pipenv run python main.py
