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
from database import supabase
import session as ss

def main():
    root = tk.Tk()
    root.title("Hockey Stats")
    root.state("zoomed")

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



    #Create match in Supabase
    match_id = ss.get_match_id()
    if match_id is None:
        try:
            team1_id, team2_id = ss.get_teams_ids()
            if team1_id and team2_id:
                match_response = supabase.table("matches").insert({
                    "team1_id": team1_id,
                    "team2_id": team2_id,
                    "team1_score": 0,
                    "team2_score": 0
                }).execute()
                match_id = match_response.data[0]["id"]
                ss.save_match_id(match_id)
        except Exception as e:
            print(f"Error creating match in database: {e}")



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
    # Check uf there is a sub
        if sub.selected_sub[0] is not None and sub.selected_team[0] == team_id:
            sub.make_substitution(team_id, player, refresh_players)
            if gs.active_frame[0]:
                gs.active_frame[0].config(highlightbackground="black", highlightthickness=2)
            gs.active_frame[0] = None
            if gs.selected_button[0]:
                gs.selected_button[0].config(bg="#B0A9A9")
            gs.selected_button[0] = None
            return

        # If not, proceed as normal
        if gs.selected_event[0] is None:
            return
        if gs.selected_event[0]["team"] != team_id:
            return

        info = gs.selected_time[0]
        event = gs.selected_event[0]

        # Handle specific events
        if event["event"] == "shot" and event.get("result") == "shot on target":
            with open("teams_data.json") as f:
                data = json.load(f)
            opposing_players_key = "players_team1" if event["opposing_team"] == "team1" else "players_team2"
            opposing_players = data.get(opposing_players_key, [])
            gk = next((p for p in opposing_players if p[3].lower() == "gk" and p[4].lower() == "yes"), None)

            stats.add_stat(event["opposing_team"], "shot", quarter=info["quarter"], time=info["time"], result="saved", player=gk[0] if gk else None, position="GK")
            stats.add_stat(event["team"], "shot", quarter=info["quarter"], time=info["time"], result="shot on target", player=player[0], position=player[3] if player[3] else None)
        elif event["event"] == "shot" and event.get("result") == "goal":
            if gs.waiting_assist[0]:
                #Assist player
                stats.add_stat(event["team"], "assist", quarter=info["quarter"], time=info["time"], player=player[0], position=player[3] if player[3] else None)
                gs.waiting_assist[0] = False
                if gs.selected_button[0]:
                    gs.selected_button[0].config(bg="#B0A9A9")
                if gs.active_frame[0]:
                    gs.active_frame[0].config(highlightbackground="black", highlightthickness=2)
                gs.selected_button[0] = None
                gs.active_frame[0] = None
                gs.selected_event[0] = None
                return
            else:
                #Goal scorer
                stats.add_stat(event["team"], "shot", quarter=info["quarter"], time=info["time"], result="goal", player=player[0], position=player[3] if player[3] else None)
                event["score_label"].config(text=str(int(event["score_label"].cget("text")) + 1))
                try:
                    match_id = ss.get_match_id()
                    if match_id:
                        supabase.rpc("update_score", {
                            "p_match_id": match_id,
                            "p_team": event["team"]
                        }).execute()
                except Exception as e:
                    print(f"Error updating score in database: {e}")
                
                #Ask for assist
                def on_yes():
                    gs.waiting_assist[0] = True
                    active = player_frame1 if event["team"] == "team1" else player_frame2
                    active.config(highlightbackground="#FFD700", highlightthickness=5)
                    gs.active_frame[0] = active
                    popup.destroy()

                def on_no():
                    gs.waiting_assist[0] = False
                    if gs.selected_button[0]:
                        gs.selected_button[0].config(bg="#B0A9A9")
                    if gs.active_frame[0]:
                        gs.active_frame[0].config(highlightbackground="black", highlightthickness=2)
                    gs.selected_button[0] = None
                    gs.active_frame[0] = None
                    gs.selected_event[0] = None
                    popup.destroy()
                
                popup = tk.Toplevel(root)
                popup.title("Assist")
                popup.geometry("300x150")
                popup.resizable(False, False)
                popup.grab_set()
                popup.update_idletasks()
                x = (popup.winfo_screenwidth() // 2) - 150
                y = (popup.winfo_screenheight() // 2) - 75
                popup.geometry(f"300x150+{x}+{y}")
                tk.Label(popup, text="Was there an assist?", font=("Arial", 12)).pack(pady=20)
                tk.Button(popup, text="Yes", font=("Arial", 10, "bold"), command=on_yes).pack(side="left", expand=True, padx=20, pady=10)
                tk.Button(popup, text="No", font=("Arial", 10, "bold"), command=on_no).pack(side="right", expand=True, padx=20, pady=10)
                return
        # PC goal
        elif event["event"] == "pc" and event.get("result") == "goal":
            if gs.waiting_assist[0]:
                stats.add_stat(event["team"], "assist", quarter=info["quarter"], time=info["time"], player=player[0], position=player[3] if player[3] else None)
                gs.waiting_assist[0] = False
                if gs.selected_button[0]:
                    gs.selected_button[0].config(bg="#B0A9A9")
                if gs.active_frame[0]:
                    gs.active_frame[0].config(highlightbackground="black", highlightthickness=2)
                gs.selected_button[0] = None
                gs.active_frame[0] = None
                gs.selected_event[0] = None
                return
            else:
                stats.add_stat(event["team"], "pc", quarter=info["quarter"], time=info["time"], result="goal", player=player[0], position=player[3] if player[3] else None)
                event["score_label"].config(text=str(int(event["score_label"].cget("text")) + 1))
                try:
                    match_id = ss.get_match_id()
                    if match_id:
                        supabase.rpc("update_score", {
                            "p_match_id": match_id,
                            "p_team": event["team"]
                        }).execute()
                except Exception as e:
                    print(f"Error updating score in database: {e}")

                def on_yes():
                    gs.waiting_assist[0] = True
                    active = player_frame1 if event["team"] == "team1" else player_frame2
                    active.config(highlightbackground="#FFD700", highlightthickness=5)
                    gs.active_frame[0] = active
                    popup.destroy()
                
                def on_no():
                    gs.waiting_assist[0] = False
                    if gs.selected_button[0]:
                        gs.selected_button[0].config(bg="#B0A9A9")
                    if gs.active_frame[0]:
                        gs.active_frame[0].config(highlightbackground="black", highlightthickness=2)
                    gs.selected_button[0] = None
                    gs.active_frame[0] = None
                    gs.selected_event[0] = None
                    popup.destroy()
                
                popup = tk.Toplevel(root)
                popup.title("Assist")
                popup.geometry("300x150")
                popup.resizable(False, False)
                popup.grab_set()
                popup.update_idletasks()
                x = (popup.winfo_screenwidth() // 2) - 150
                y = (popup.winfo_screenheight() // 2) - 75
                popup.geometry(f"300x150+{x}+{y}")
                tk.Label(popup, text="Was there an assist?", font=("Arial", 12)).pack(pady=20)
                tk.Button(popup, text="Yes", font=("Arial", 10, "bold"), command=on_yes).pack(side="left", expand=True, padx=20, pady=10)
                tk.Button(popup, text="No", font=("Arial", 10, "bold"), command=on_no).pack(side="right", expand=True, padx=20, pady=10)
                return
        elif event["event"] == "pc" and event.get("result") == "saved":
            with open("teams_data.json") as f:
                data = json.load(f)
            opposing_players_key = "players_team1" if event["opposing_team"] == "team1" else "players_team2"
            opposing_players = data.get(opposing_players_key, [])
            gk = next((p for p in opposing_players if p[3].lower() == "gk" and p[4].lower() == "yes"), None)
            stats.add_stat(event["opposing_team"], "pc", quarter=info["quarter"], time=info["time"], result="saved", player=gk[0] if gk else None, position="GK")
            stats.add_stat(event["team"], "pc", quarter=info["quarter"], time=info["time"], result="shot on target", player=player[0], position=player[3] if player[3] else None)
        else:
            stats.add_stat(event["team"], event["event"], quarter=info["quarter"], time=info["time"], result=event.get("result"), player=player[0], position=player[3] if player[3] else None)

        # Reset
        if gs.selected_button[0]:
            gs.selected_button[0].config(bg="#B0A9A9", highlightthickness=2)
        if gs.active_frame[0]:
            gs.active_frame[0].config(highlightbackground="black", highlightthickness=2)
        gs.active_frame[0] = None
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
            command=lambda: sub.show_subs(root, "team1", refresh_players)).pack(side="bottom", pady=10)

        tk.Label(player_frame2, text="Players", font=("Arial", 14, "bold")).pack(pady=10)
        for p in p2:
            if p[4].lower() == "yes" and p[1] and p[2]:
                tk.Button(player_frame2, text=f"{p[0]} - {p[1][0]}. {p[2]}", font=("Arial", 12, "bold"),
                    command=lambda pl=p: on_player_click(pl, "team2")).pack(pady=7)
        tk.Button(player_frame2, text="Subs", font=("Arial", 12, "bold"), bg="#B0A9A9",
            command=lambda: sub.show_subs(root, "team2", refresh_players)).pack(side="bottom", pady=10)

    player_frame1 = tk.Frame(root, highlightbackground="black", highlightthickness=2)
    player_frame1.place(x=50, y=150, width=200, height=630)
    player_frame2 = tk.Frame(root, highlightbackground="black", highlightthickness=2)
    player_frame2.place(x=1250, y=150, width=200, height=630)

    refresh_players()


    # Buttons team 1
    tc.setup_goal(root, get_quarter_time, score1_label, "team1", 310, player_frame1, player_frame2)
    tc.setup_shot(root, get_quarter_time, "team1", "team2", 310, player_frame1, player_frame2)
    tc.setup_foul(root, get_quarter_time, "team1", 310, player_frame1, player_frame2)
    tc.setup_pc(root, get_quarter_time, score1_label, "team1", "team2", 310, player_frame1, player_frame2)
    tc.setup_corner(root, get_quarter_time, "team1", 310, player_frame1, player_frame2)

    # Buttons team 2
    tc.setup_goal(root, get_quarter_time, score2_label, "team2", 1100, player_frame1, player_frame2)
    tc.setup_shot(root, get_quarter_time, "team2", "team1", 1100, player_frame1, player_frame2)
    tc.setup_foul(root, get_quarter_time, "team2", 1100, player_frame1, player_frame2)
    tc.setup_pc(root, get_quarter_time, score2_label, "team2", "team1", 1100, player_frame1, player_frame2)
    tc.setup_corner(root, get_quarter_time, "team2", 1100, player_frame1, player_frame2)

    # Reset stats button (Temporary, for testing purposes)
    def reset_stats():
        stats.reset_stats()
        score1_label.config(text="0")
        score2_label.config(text="0")
    tk.Button(root, text="Reset Stats", font=("Arial", 10, "bold"), bg="#FF6B6B", command=reset_stats).place(x=700, y=750, width=100, height=40)

    root.mainloop()

if __name__ == "__main__":
    main()