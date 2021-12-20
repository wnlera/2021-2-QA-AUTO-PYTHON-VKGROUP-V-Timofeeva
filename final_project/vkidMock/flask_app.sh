#!/bin/ash
pip install -r /app/requirements.txt
FLASK_APP=/app/app.py FLASK_ENV=development flask run --port 5001 --host=0.0.0.0