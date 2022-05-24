#!/usr/bin/env bash

export FLASK_APP=app.py
export FLASK_ENV=development

export DB_HOST=""
export SECRET_KEY=""

flask run --host=0.0.0.0
