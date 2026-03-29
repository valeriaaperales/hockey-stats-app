import tkinter as tk
import game_state as gs

# Goal
def setup_goal(root, score_label, team_id, x_pos):
    def add_goal():
        if gs.selected_button[0]:
            gs.selected_button[0].config(bg="#B0A9A9")
        goal.config(bg="#FFD700")
        gs.selected_button[0] = goal
        gs.selected_event[0] = {"team": team_id, "event": "shot", "result": "goal", "score_label": score_label}
    goal = tk.Button(root, text="Goal", font=("Arial", 12, "bold"), command=add_goal, bg="#B0A9A9")
    goal.place(x=x_pos, y=280, width=100, height=80)

# Shot
def setup_shot(root, team_id, opposing_team_id, x_pos):
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
            shot.config(bg="#FFD700")
            gs.selected_button[0] = shot
            gs.selected_event[0] = {"team": team_id, "event": "shot", "result": "miss", "opposing_team": opposing_team_id}
            popup.destroy()

        def select_save():
            if gs.selected_button[0]:
                gs.selected_button[0].config(bg="#B0A9A9")
            shot.config(bg="#FFD700")
            gs.selected_button[0] = shot
            gs.selected_event[0] = {"team": team_id, "event": "shot", "result": "shot on target", "opposing_team": opposing_team_id}
            popup.destroy()

        tk.Label(popup, text="Select shot result:", font=("Arial", 12)).pack(pady=10)
        tk.Button(popup, text="Miss", font=("Arial", 10), command=select_miss).pack(pady=5)
        tk.Button(popup, text="Saved", font=("Arial", 10), command=select_save).pack(pady=5)

    shot = tk.Button(root, text="Shot", font=("Arial", 12, "bold"), command=add_shot, bg="#B0A9A9")
    shot.place(x=x_pos, y=380, width=100, height=80)

# Foul
def setup_foul(root, team_id, x_pos):
    def add_foul():
        if gs.selected_button[0]:
            gs.selected_button[0].config(bg="#B0A9A9")
        foul.config(bg="#FFD700")
        gs.selected_button[0] = foul
        gs.selected_event[0] = {"team": team_id, "event": "foul"}
    foul = tk.Button(root, text="Foul", font=("Arial", 12, "bold"), command=add_foul, bg="#B0A9A9")
    foul.place(x=x_pos, y=480, width=100, height=80)

# PC
def setup_pc(root, team_id, x_pos):
    def add_pc():
        if gs.selected_button[0]:
            gs.selected_button[0].config(bg="#B0A9A9")
        pc.config(bg="#FFD700")
        gs.selected_button[0] = pc
        gs.selected_event[0] = {"team": team_id, "event": "pc"}
    pc = tk.Button(root, text="PC", font=("Arial", 12, "bold"), command=add_pc, bg="#B0A9A9")
    pc.place(x=x_pos, y=580, width=100, height=80)

# Corner
def setup_corner(root, team_id, x_pos):
    def add_corner():
        if gs.selected_button[0]:
            gs.selected_button[0].config(bg="#B0A9A9")
        corner.config(bg="#FFD700")
        gs.selected_button[0] = corner
        gs.selected_event[0] = {"team": team_id, "event": "corner"}
    corner = tk.Button(root, text="Corner", font=("Arial", 12, "bold"), command=add_corner, bg="#B0A9A9")
    corner.place(x=x_pos, y=680, width=100, height=80)
