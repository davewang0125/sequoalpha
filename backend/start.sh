#!/bin/bash njujunuunu

# Initialize the database
python init_db.py

# Start the application
gunicorn main:app --bind 0.0.0.0:$PORT
