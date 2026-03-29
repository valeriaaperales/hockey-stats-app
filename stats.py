import json
import os

stats_file = "stats_data.json"
teams_file = "teams_data.json"

def get_teams_names():
    if os.path.exists(teams_file):
        with open(teams_file) as f:
            data = json.load(f)
        return data.get("team1_name", "Team 1"), data.get("team2_name", "Team 2")
    return "Team 1", "Team 2"

def load_stats():
    team1, team2 = get_teams_names()
    if os.path.exists(stats_file):
        with open(stats_file) as f:
            return json.load(f)
    return {team1: [], team2: []}

def save_stats(stats):
    with open(stats_file, "w") as f:
        json.dump(stats, f, indent=2)

def add_stat(team: str, event: str, quarter: str = None, time: str = None, result: str = None, player: str = None):
    team1, team2 = get_teams_names()
    team_name = team1 if team == "team1" else team2

    data = load_stats()
    if team_name not in data:
        data[team_name] = []

    entry = {
        "event": event,
        "quarter": quarter,
        "time": time,
        "result": result if event in ["shot", "save"] else None,
        "player": player
    }
    data[team_name].append(entry)
    save_stats(data)

def reset_stats():
    team1, team2 = get_teams_names()
    save_stats({team1: [], team2: []})

def get_stats(team: str, event: str) -> int:
    stats = load_stats()
    if team not in stats:
        return 0
    return sum(1 for entry in stats[team] if entry["event"] == event)  