# 🏑 Hockey Stats App — In Progress

Desktop application for real-time field hockey match statistics tracking, built with Python and Tkinter.

## Features
- Track goals, shots, fouls, PCs and corners per team
- Real-time score tracking
- Player roster management with starters and substitutes
- Statistics saved locally in JSON (planned migration to Supabase)
- Quarter and time tracking per event

## Requirements
- Python 3.x
- tkinter (included with Python)

## How to run
```
python teams_data.py
```
Start by entering the team names and players, then the match screen will open automatically.

## File structure
```
hockey_app/
├── main.py              ← match screen
├── teams_data.py        ← team and player setup
├── team1_buttons.py     ← team 1 stat buttons
├── team2_buttons.py     ← team 2 stat buttons
├── timer_quarter.py     ← match timer
├── stats.py             ← statistics logic
└── subs.py              ← substitutions
```

## Planned
- Supabase cloud database for multi-device sync
- Interactive dashboards for coaches