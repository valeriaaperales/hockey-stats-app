import tkinter as tk
import json
import os
import subprocess
import sys
import stats
import game_state as gs
import timer_quarter as timer
import team_controls as tc
import sub as sub

def main():
    root = tk.Tk()
    root.title("Hockey Stats")
    root.geometry("1500x800")

    # Load team data
    colors_hex = {
        "Red": "#FF0000", "Blue": "#0000FF", "Green": "#00AA00",
        "Yellow": "#FFD700", "Black": "#000000", "White": "#FFFFFF"
    }
    team1_name, team2_name = "Team 1", "Team 2"
    team1_color, team2_color = "#FFFFFF", "#FFFFFF"

    if os.path.exists("teams_data.json"):
        with open("teams_data.json") as f:
            data = json.load(f)
        team1_name = data.get("team1_name", "Team 1")
        team2_name = data.get("team2_name", "Team 2")
        team1_color = colors_hex.get(data.get("team1_color"), "#FFFFFF")
        team2_color = colors_hex.get(data.get("team2_color"), "#FFFFFF")
        players_team1 = data.get("players_team1", [])
        players_team2 = data.get("players_team2", [])

    # Timer
    get_quarter_time = timer.setup_timer(root)

    # Teams frame
    team1_text_color = "black" if team1_color == "#FFFFFF" else "white"
    team2_text_color = "black" if team2_color == "#FFFFFF" else "white"

    team1_frame = tk.Frame(root, highlightbackground="black", highlightthickness=2, bg=team1_color)
    team1_frame.place(x=50, y=50, width=300, height=80)
    tk.Label(team1_frame, text=team1_name, font=("Arial", 18, "bold"), fg=team1_text_color, bg=team1_color).place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    team2_frame = tk.Frame(root, highlightbackground="black", highlightthickness=2, bg=team2_color)
    team2_frame.place(x=1150, y=50, width=300, height=80)
    tk.Label(team2_frame, text=team2_name, font=("Arial", 18, "bold"), fg=team2_text_color, bg=team2_color).place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    # Score frames
    score1_frame = tk.Frame(root, highlightbackground="black", highlightthickness=2, bg="#ffffff")
    score1_frame.place(x=351, y=50, width=100, height=80)
    score1_label = tk.Label(score1_frame, text="0", font=("Arial", 18, "bold"), fg="black", bg="#ffffff")
    score1_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    score2_frame = tk.Frame(root, highlightbackground="black", highlightthickness=2, bg="#ffffff")
    score2_frame.place(x=1049, y=50, width=100, height=80)
    score2_label = tk.Label(score2_frame, text="0", font=("Arial", 18, "bold"), fg="black", bg="#ffffff")
    score2_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    # Possession frames
    possession1_frame = tk.Frame(root, highlightbackground="black", highlightthickness=2, bg="#ffffff")
    possession1_frame.place(x=280, y=150, width=240, height=100)
    tk.Label(possession1_frame, text="Possession", font=("Arial", 14, "bold"), fg="black", bg="#ffffff").place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    possession2_frame = tk.Frame(root, highlightbackground="black", highlightthickness=2, bg="#ffffff")
    possession2_frame.place(x=980, y=150, width=240, height=100)
    tk.Label(possession2_frame, text="Possession", font=("Arial", 14, "bold"), fg="black", bg="#ffffff").place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    # Field
    field_w, field_h = 596, 357.6
    canvas = tk.Canvas(root, bg="#ffffff", highlightbackground="black", highlightthickness=2)
    canvas.place(x=452, y=315, width=field_w, height=field_h)
    canvas.create_rectangle(0, 0, field_w, field_h, fill="#0cdb0c")
    canvas.create_line(field_w * 0.25, 0, field_w * 0.25, field_h, fill="white", width=2)
    canvas.create_line(field_w * 0.5, 0, field_w * 0.5, field_h, fill="white", width=2)
    canvas.create_line(field_w * 0.75, 0, field_w * 0.75, field_h, fill="white", width=2)
    cy, r = field_h / 2, field_h * 0.25
    canvas.create_arc(0 - r, cy - r, 0 + r, cy + r, start=-90, extent=180, outline="white", width=2, style="arc")
    canvas.create_arc(field_w - r, cy - r, field_w + r, cy + r, start=90, extent=180, outline="white", width=2, style="arc")

    # Player click
    def on_player_click(player, team_id):
        if gs.selected_event[0] is None:
            return
        if gs.selected_event[0]["team"] != team_id:
            return

        info = get_quarter_time()
        event = gs.selected_event[0]

        if event["event"] == "shot" and event.get("result") == "shot on target":
            stats.add_stat(event["opposing_team"], "save", quarter=info["quarter"], time=info["time"], result="saved", player=player[0])
            stats.add_stat(event["team"], "shot", quarter=info["quarter"], time=info["time"], result="shot on target", player=player[0])
        elif event["event"] == "shot" and event.get("result") == "goal":
            stats.add_stat(event["team"], "shot", quarter=info["quarter"], time=info["time"], result="goal", player=player[0])
            event["score_label"].config(text=str(int(event["score_label"].cget("text")) + 1))
        else:
            stats.add_stat(event["team"], event["event"], quarter=info["quarter"], time=info["time"], result=event.get("result"), player=player[0])

        # Reset
        if gs.selected_button[0]:
            gs.selected_button[0].config(bg="#B0A9A9")
        gs.selected_button[0] = None
        gs.selected_event[0] = None

    # Players
    def refresh_players():
        with open("teams_data.json") as f:
            data = json.load(f)
        p1 = data.get("players_team1", [])
        p2 = data.get("players_team2", [])

        for widget in player_frame1.winfo_children():
            widget.destroy()
        for widget in player_frame2.winfo_children():
            widget.destroy()

        tk.Label(player_frame1, text="Players", font=("Arial", 14, "bold")).pack(pady=10)
        for p in p1:
            if p[4].lower() == "yes" and p[1] and p[2]:
                tk.Button(player_frame1, text=f"{p[0]} - {p[1][0]}. {p[2]}", font=("Arial", 12, "bold"),
                    command=lambda pl=p: on_player_click(pl, "team1")).pack(pady=7)
        tk.Button(player_frame1, text="Subs", font=("Arial", 12, "bold"), bg="#B0A9A9",
            command=lambda: sub.show_subs(root, 1, refresh_players)).pack(side="bottom", pady=10)

        tk.Label(player_frame2, text="Players", font=("Arial", 14, "bold")).pack(pady=10)
        for p in p2:
            if p[4].lower() == "yes" and p[1] and p[2]:
                tk.Button(player_frame2, text=f"{p[0]} - {p[1][0]}. {p[2]}", font=("Arial", 12, "bold"),
                    command=lambda pl=p: on_player_click(pl, "team2")).pack(pady=7)
        tk.Button(player_frame2, text="Subs", font=("Arial", 12, "bold"), bg="#B0A9A9",
            command=lambda: sub.show_subs(root, 2, refresh_players)).pack(side="bottom", pady=10)

    player_frame1 = tk.Frame(root, highlightbackground="black", highlightthickness=2)
    player_frame1.place(x=50, y=150, width=200, height=630)
    player_frame2 = tk.Frame(root, highlightbackground="black", highlightthickness=2)
    player_frame2.place(x=1250, y=150, width=200, height=630)

    refresh_players()

    # Buttons team 1
    tc.setup_goal(root, score1_label, "team1", 310)
    tc.setup_shot(root, "team1", "team2", 310)
    tc.setup_foul(root, "team1", 310)
    tc.setup_pc(root, "team1", 310)
    tc.setup_corner(root, "team1", 310)

    # Buttons team 2
    tc.setup_goal(root, score2_label, "team2", 1100)
    tc.setup_shot(root, "team2", "team1", 1100)
    tc.setup_foul(root, "team2", 1100)
    tc.setup_pc(root, "team2", 1100)
    tc.setup_corner(root, "team2", 1100)

    # Reset stats button (Temporary, for testing purposes)
    tk.Button(root, text="Reset Stats", font=("Arial", 10, "bold"), bg="#FF6B6B", command=stats.reset_stats).place(x=700, y=750, width=100, height=40)

    root.mainloop()

if __name__ == "__main__":
    main()