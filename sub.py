import tkinter as tk
import json
import os

selected_sub = [None]
selected_team = [None]

# Show substitutions
def show_subs(root, team, refresh_callback):
    if not os.path.exists("teams_data.json"):
        return
    with open("teams_data.json") as f:
        data = json.load(f)

    players_key = "players_team1" if team == "team1" else "players_team2"
    players = data.get(players_key, [])
    subs = [p for p in players if p[4].lower() != "yes" and p[1] and p[2]]

    popup = tk.Toplevel(root)
    popup.title(f"Substitutions")
    popup.geometry("300x400")
    popup.resizable(False, False)
    popup.update_idletasks()
    y = (popup.winfo_screenheight() // 2) - 200
    if team == "team1":  # Left side of the screen
        x = 50
    else:  # Right side of the screen
        x = popup.winfo_screenwidth() - 350
    popup.geometry(f"300x400+{x}+{y}")

    tk.Label(popup, text="Select sub to enter:", font=("Arial", 14, "bold")).pack(pady=10)

    if not subs:
        tk.Label(popup, text="No substitutions available", font=("Arial", 12)).pack(pady=20)
    else:
        for s in subs:
            def select_sub(player=s):
                selected_sub[0] = player
                selected_team[0] = team
                popup.destroy()
            tk.Button(popup, text=f"{s[0]} - {s[1][0]}. {s[2]}", font=("Arial", 12, "bold"),
                bg="#B0A9A9", command=select_sub).pack(pady=5, fill="x", padx=10)

# Make substitution
def make_substitution(team, player_out, refresh_callback):
    if selected_sub[0] is None or selected_team[0] != team:
        return
    if not os.path.exists("teams_data.json"):
        return
    with open("teams_data.json") as f:
        data = json.load(f)

    players_key = "players_team1" if team == "team1" else "players_team2"
    players = data.get(players_key, [])

    for player in players:
        if player[0] == player_out[0]:  # Player going out
            player[4] = "No"
        if player[0] == selected_sub[0][0]:  # Player coming in
            player[4] = "Yes"

    with open("teams_data.json", "w") as f:
        json.dump(data, f, indent=4)

    selected_sub[0] = None
    selected_team[0] = None

    try:
        from database import supabase
        import session as ss
        team1_id, team2_id = ss.get_teams_ids()
        team_id = team1_id if team == "team1" else team2_id
        if team_id:
            supabase.rpc("make_substitution", {
                "p_team_id": team_id,
                "p_player_out": int(player_out[0]),
                "p_player_in": int(selected_sub[0][0])
            }).execute()
    except Exception as e:
        print(f"Error making substitution in database: {e}")

    refresh_callback()