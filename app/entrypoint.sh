#!/bin/bash

# Start Flask in debug mode
export FLASK_APP=app.py
export FLASK_ENV=development
flask run --host=0.0.0.0
