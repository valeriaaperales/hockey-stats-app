import json
import os

SESSION_FILE = "session.json"

def save_match_id(match_id: int):
    data = load_session()
    data["match_id"] = match_id
    _save(data)

def get_match_id():
    return load_session().get("match_id", None)

def save_teams_ids(team1_id: int, team2_id: int):
    data = load_session()
    data["team1_id"] = team1_id
    data["team2_id"] = team2_id
    _save(data)

def get_teams_ids():
    data = load_session()
    return data.get("team1_id"), data.get("team2_id")

def load_session():
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, "r") as f:
            return json.load(f)
    return {}

def _save(data):
    with open(SESSION_FILE, "w") as f:
        json.dump(data, f)