import tkinter as tk
import game_state as gs

# Goal
def setup_goal(root, get_quarter_time, score_label, team_id, x_pos, frame_1, frame_2):
    def add_goal():
        if gs.selected_button[0]:
            gs.selected_button[0].config(bg="#B0A9A9")
        if gs.active_frame[0]:
            gs.active_frame[0].config(highlightbackground="black")
        goal.config(bg="#FFD700")
        gs.selected_button[0] = goal
        gs.selected_event[0] = {"team": team_id, "event": "shot", "result": "goal", "score_label": score_label, "waiting_assist": False}
        gs.selected_time[0] = get_quarter_time()
        active = frame_1 if team_id == "team1" else frame_2
        active.config(highlightbackground="#FFD700", highlightthickness=5)
        gs.active_frame[0] = active

    goal = tk.Button(root, text="Goal", font=("Arial", 12, "bold"), command=add_goal, bg="#B0A9A9")
    goal.place(x=x_pos, y=210, width=100, height=80)

# Shot
def setup_shot(root, get_quarter_time, team_id, opposing_team_id, x_pos, frame_1, frame_2):
    def add_shot():
        popup = tk.Toplevel(root)
        popup.title("Shot Result")
        popup.geometry("300x150")
        popup.resizable(False, False)
        popup.grab_set()
        popup.update_idletasks()
        x = (popup.winfo_screenwidth() // 2) - 150
        y = (popup.winfo_screenheight() // 2) - 75
        popup.geometry(f"300x150+{x}+{y}")

        def select_miss():
            if gs.selected_button[0]:
                gs.selected_button[0].config(bg="#B0A9A9")
            if gs.active_frame[0]:
                gs.active_frame[0].config(highlightbackground="black")
            shot.config(bg="#FFD700")
            gs.selected_button[0] = shot
            gs.selected_event[0] = {"team": team_id, "event": "shot", "result": "miss", "opposing_team": opposing_team_id}
            active = frame_1 if team_id == "team1" else frame_2
            active.config(highlightbackground="#FFD700", highlightthickness=5)
            gs.active_frame[0] = active
            popup.destroy()

        def select_save():
            if gs.selected_button[0]:
                gs.selected_button[0].config(bg="#B0A9A9")
            if gs.active_frame[0]:
                gs.active_frame[0].config(highlightbackground="black")
            shot.config(bg="#FFD700")
            gs.selected_button[0] = shot
            gs.selected_event[0] = {"team": team_id, "event": "shot", "result": "shot on target", "opposing_team": opposing_team_id}
            active = frame_1 if team_id == "team1" else frame_2
            active.config(highlightbackground="#FFD700", highlightthickness=5)
            gs.active_frame[0] = active
            popup.destroy()

        gs.selected_time[0] = get_quarter_time()

        tk.Label(popup, text="Select shot result:", font=("Arial", 12)).pack(pady=10)
        tk.Button(popup, text="Miss", font=("Arial", 10), command=select_miss).pack(pady=5)
        tk.Button(popup, text="Saved", font=("Arial", 10), command=select_save).pack(pady=5)

    shot = tk.Button(root, text="Shot", font=("Arial", 12, "bold"), command=add_shot, bg="#B0A9A9")
    shot.place(x=x_pos, y=310, width=100, height=80)

# Foul
def setup_foul(root, get_quarter_time, team_id, x_pos, frame_1, frame_2):
    def add_foul():
        if gs.selected_button[0]:
            gs.selected_button[0].config(bg="#B0A9A9")
        if gs.active_frame[0]:
            gs.active_frame[0].config(highlightbackground="black")
        foul.config(bg="#FFD700")
        gs.selected_button[0] = foul
        gs.selected_event[0] = {"team": team_id, "event": "foul"}
        gs.selected_time[0] = get_quarter_time()
        active = frame_1 if team_id == "team1" else frame_2
        active.config(highlightbackground="#FFD700", highlightthickness=5)
        gs.active_frame[0] = active

    foul = tk.Button(root, text="Foul", font=("Arial", 12, "bold"), command=add_foul, bg="#B0A9A9")
    foul.place(x=x_pos, y=410, width=100, height=80)

# PC
def setup_pc(root, get_quarter_time, score_label, team_id, opposing_team_id, x_pos, frame_1, frame_2):
    def add_pc():
        popup = tk.Toplevel(root)
        popup.title("Penalty Corner")
        popup.geometry("300x200")
        popup.resizable(False, False)
        popup.grab_set()
        popup.update_idletasks()
        x = (popup.winfo_screenwidth() // 2) - 150
        y = (popup.winfo_screenheight() // 2) - 100
        popup.geometry(f"300x200+{x}+{y}")

        def select_pc_goal():
            if gs.selected_button[0]:
                gs.selected_button[0].config(bg="#B0A9A9")
            if gs.active_frame[0]:
                gs.active_frame[0].config(highlightbackground="black")
            pc.config(bg="#FFD700")
            gs.selected_button[0] = pc
            gs.selected_event[0] = {"team": team_id, "event": "pc", "result": "goal", "score_label": score_label}
            gs.selected_time[0] = get_quarter_time()
            active = frame_1 if team_id == "team1" else frame_2
            active.config(highlightbackground="#FFD700", highlightthickness=5)
            gs.active_frame[0] = active
            popup.destroy()
        
        def select_pc_miss():
            if gs.selected_button[0]:
                gs.selected_button[0].config(bg="#B0A9A9")
            if gs.active_frame[0]:
                gs.active_frame[0].config(highlightbackground="black")
            pc.config(bg="#FFD700")
            gs.selected_button[0] = pc
            gs.selected_event[0] = {"team": team_id, "event": "pc", "result": "miss"}
            gs.selected_time[0] = get_quarter_time()
            active = frame_1 if team_id == "team1" else frame_2
            active.config(highlightbackground="#FFD700", highlightthickness=5)
            gs.active_frame[0] = active
            popup.destroy()

        def select_pc_saved():
            if gs.selected_button[0]:
                gs.selected_button[0].config(bg="#B0A9A9")
            if gs.active_frame[0]:
                gs.active_frame[0].config(highlightbackground="black")
            pc.config(bg="#FFD700")
            gs.selected_button[0] = pc
            gs.selected_event[0] = {"team": team_id, "event": "pc", "result": "saved", "opposing_team": opposing_team_id}
            gs.selected_time[0] = get_quarter_time()
            active = frame_1 if team_id == "team1" else frame_2
            active.config(highlightbackground="#FFD700", highlightthickness=5)
            gs.active_frame[0] = active
            popup.destroy()

        def select_another_pc():
            if gs.selected_button[0]:
                gs.selected_button[0].config(bg="#B0A9A9")
            if gs.active_frame[0]:
                gs.active_frame[0].config(highlightbackground="black")
            pc.config(bg="#B0A9A9")
            gs.selected_button[0] = None
            gs.active_frame[0] = None
            info = get_quarter_time()
            import stats
            stats.add_stat(team_id, "pc", quarter=info["quarter"], time=info["time"], result="another pc")
            popup.destroy()           
        
        tk.Label(popup, text="Select PC result:", font=("Arial", 12)).pack(pady=10)
        tk.Button(popup, text="Goal", font=("Arial", 10), command=select_pc_goal).pack(pady=5)
        tk.Button(popup, text="Miss", font=("Arial", 10), command=select_pc_miss).pack(pady=5)
        tk.Button(popup, text="Saved", font=("Arial", 10), command=select_pc_saved).pack(pady=5)
        tk.Button(popup, text="Another PC", font=("Arial", 10), command=select_another_pc).pack(pady=5)

    pc = tk.Button(root, text="PC", font=("Arial", 12, "bold"), command=add_pc, bg="#B0A9A9")
    pc.place(x=x_pos, y=510, width=100, height=80)

# Corner
def setup_corner(root, get_quarter_time, team_id, x_pos, frame_1, frame_2):
    def add_corner():
        if gs.selected_button[0]:
            gs.selected_button[0].config(bg="#B0A9A9")
        if gs.active_frame[0]:
            gs.active_frame[0].config(highlightbackground="black")
        gs.selected_button[0] = None
        gs.active_frame[0] = None

        info = get_quarter_time()
        import stats
        stats.add_stat(team_id, "corner", quarter=info["quarter"], time=info["time"])

    corner = tk.Button(root, text="Corner", font=("Arial", 12, "bold"), command=add_corner, bg="#B0A9A9")
    corner.place(x=x_pos, y=610, width=100, height=80)

def setup_entry(root, get_quarter_time, team_id, x_pos, frame_1, frame_2):
    def add_entry():
        if gs.selected_button[0]:
            gs.selected_button[0].config(bg="#B0A9A9")
        if gs.active_frame[0]:
            gs.active_frame[0].config(highlightbackground="black")
        gs.selected_button[0] = None
        gs.active_frame[0] = None

        info = get_quarter_time()
        import stats
        stats.add_stat(team_id, "entry", quarter=info["quarter"], time=info["time"])

    entry = tk.Button(root, text="Circle Entry", font=("Arial", 12, "bold"), command=add_entry, bg="#B0A9A9")
    entry.place(x=x_pos, y=710, width=100, height=80)