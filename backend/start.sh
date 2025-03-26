#!/bin/bash

# Activate the virtual environment
source venv/bin/activate

# Start the server
uvicorn app.main:app --reload --port 8000

# If you're having issues, try running these commands manually:
# cd backend
# source venv/bin/activate
# python -m uvicorn app.main:app --reload --port 8000 