import tkinter as tk
import json
import os

def show_subs(root, team):
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
            tk.Button(popup, text=f"{sub[0]}", font=("Arial", 12)).pack(pady=5)
