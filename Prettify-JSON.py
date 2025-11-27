#!/usr/bin/python3
import json

# Load JSON data from file
with open('credentials.json', 'r') as f:

    data = json.load(f)
    client_id = data["installed"]["client_id"]
    client_secret = data["installed"]["client_secret"]
    project_id = data["installed"]["project_id"]
    refresh_token = data["installed"]["refresh_token"]

    print(f"Your client_id: {client_id}")
    print(f"Your client_secret: {client_secret}")
    print(f"Your project_id: {project_id}")
    print(f"Your refresh_token: {refresh_token}")

