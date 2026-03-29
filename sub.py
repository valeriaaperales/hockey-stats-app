import tkinter as tk
import json
import os

selected_sub = [None]
selected_team = [None]

#Show substitutions
def show_subs(root, team, refresh_callback):
    if not os.path.exists("teams_data.json"):
        return
    with open("teams_data.json") as f:
        data = json.load(f)
    
    players_key = "players_team1" if team == 1 else "players_team2"
    players = data.get(players_key, [])
    subs = [p for p in players if p[4] != "Yes" and p[4] != 'yes' and p[1] and p[2]]

    popup = tk.Toplevel(root)
    popup.title(f"Substitutions - Team {team}")
    popup.geometry("400x300")
    popup.resizable(False, False)
    popup.grab_set()  # Make the popup modal
    popup.update_idletasks()
    y = (popup.winfo_screenheight() // 2) - (300 // 2)
    if team == 1: #Left side of the screen
        x = 50
    else: #Right side of the screen
        x = popup.winfo_screenwidth() - 450
    popup.geometry(f"400x300+{x}+{y}")
    tk.Label(popup, text=f"Substitutions - Team {team}", font=("Arial", 14, "bold")).pack(pady=10)

    if not subs:
        tk.Label(popup, text="No substitutions available", font=("Arial", 12)).pack(pady=20)
    else:
        for sub in subs:
            def select_sub(s=sub):
                selected_sub[0] = s
                selected_team[0] = team
                popup.destroy()
            tk.Button(popup, text=f"{sub[0]}", font=("Arial", 12), command=select_sub).pack(pady=5)

#Select sub for starter
def make_substitution(team, player_out, refresh_callback):
    if selected_sub[0] is None or selected_team[0] != team:
        return
    if not os.path.exists("teams_data.json"):
        return
    with open("teams_data.json") as f:
        data = json.load(f)
    
    players_key = "players_team1" if team == 1 else "players_team2"
    players = data.get(players_key, [])
    
    for player in players:
        if player[0] == player_out[0]:
            player[4] = "No"
        if player[0] == selected_sub[0][0]:
            player[4] = "Yes"
    
    with open("teams_data.json", "w") as f:
        json.dump(data, f, indent=4)
    
    selected_sub[0] = None
    selected_team[0] = None
    refresh_callback()
