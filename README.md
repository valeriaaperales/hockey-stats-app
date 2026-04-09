# 🏑 Hockey Stats App

Desktop application for real-time field hockey match statistics tracking, built with Python and Tkinter, with cloud synchronization via Supabase.

## Features
- Track goals, shots, fouls, penalty corners and corners per team
- Real-time score tracking
- Player roster management with starters and substitutes
- Substitution handling
- Assist tracking for goals and penalty corner goals
- Statistics saved locally in JSON and synced to Supabase
- Quarter and time tracking per event
- Multi-device synchronization via Supabase

## Requirements
- Python 3.x
- tkinter (included with Python)
- supabase-py (optional, for cloud synchronization)

```
pip install supabase
```

## Configuration
Supabase integration is optional. The app works fully offline using local JSON files.

To enable cloud synchronization, create a `config.py` file in the root directory with your Supabase credentials:

```python
SUPABASE_URL = "your_supabase_url"
SUPABASE_KEY_SERVICE_ROLE = "your_service_role_key"
```

This file is listed in `.gitignore` and should never be committed to version control.
## How to run
```
python team_data.py
```
Start by entering the team names, colors and players. The match screen will open automatically.

## File structure
```
hockey_app/
├── main.py              ← match screen and main window
├── team_data.py         ← team and player setup
├── team_controls.py     ← event buttons (goals, shots, fouls, PCs, corners)
├── timer_quarter.py     ← match timer with quarter tracking
├── stats.py             ← statistics logic and local persistence
├── sub.py               ← substitution handling
├── game_state.py        ← in-memory game state
├── session.py           ← session management (match and team IDs)
├── database.py          ← Supabase client
├── config.py            ← Supabase credentials (not in version control)
├── hockey_supabase.sql  ← database schema and RPC functions
├── teams_data.json      ← local team and player data (not in version control)
├── stats_data.json      ← local stats data (not in version control)
└── session.json         ← local session data (not in version control)
```

## Database schema
The Supabase database consists of four tables: `teams`, `players`, `matches` and `events`. The schema and RPC functions are defined in `hockey_supabase.sql`.

RPC functions:
- `insert_event` — inserts a match event resolving team and player IDs internally
- `update_score` — increments the score for a team in a match
- `update_starter` — updates starter status when a substitution is made

## Planned
- Undo last action button
- Role-based access control (Coach 1, Coach 2, Data Operator)
- Stroke penalty corner tracking
- Web dashboard for real-time match visualization and post-match analysis