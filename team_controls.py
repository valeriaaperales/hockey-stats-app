import tkinter as tk
import stats

# Goal
def setup_goal(root, get_quarter_time, score_label, team_id, x_pos):
    def add_goal():
        info = get_quarter_time()
        stats.add_stat(team_id, "shot", quarter=info["quarter"], time=info["time"], result="goal")
        score = int(score_label.cget("text"))
        score_label.config(text=str(score + 1))
    tk.Button(root, text="Goal", font=("Arial", 12, "bold"), command=add_goal, bg="#B0A9A9").place(x=x_pos, y=280, width=100, height=80)

# Shot
def setup_shot(root, get_quarter_time, team_id, opposing_team_id, x_pos):
    def add_shot():
        popup = tk.Toplevel(root)
        popup.title("Shot Result")
        popup.geometry("300x150")
        popup.resizable(False, False)
        popup.grab_set()  # Make the popup modal
        
        # Center the popup on the screen
        popup.update_idletasks()
        x = (popup.winfo_screenwidth() // 2) - (300 // 2)
        y = (popup.winfo_screenheight() // 2) - (150 // 2)
        popup.geometry(f"300x150+{x}+{y}")

        def add_miss():
            info = get_quarter_time()
            stats.add_stat(team_id, "shot", quarter=info["quarter"], time=info["time"], result="miss")
            popup.destroy()

        def add_save():
            info = get_quarter_time()
            stats.add_stat(opposing_team_id, "save", quarter=info["quarter"], time=info["time"], result="saved")
            stats.add_stat(team_id, "shot", quarter=info["quarter"], time=info["time"], result="shot on target")
            popup.destroy()

        tk.Label(popup, text="Select shot result:", font=("Arial", 12)).pack(pady=10)
        tk.Button(popup, text="Miss", font=("Arial", 10), command=add_miss).pack(pady=5)
        tk.Button(popup, text="Saved", font=("Arial", 10), command=add_save).pack(pady=5)

    tk.Button(root, text="Shot", font=("Arial", 12, "bold"), command=add_shot, bg="#B0A9A9").place(x=x_pos, y=380, width=100, height=80)

# Foul
def setup_foul(root, get_quarter_time, team_id, x_pos):
    def add_foul():
        info = get_quarter_time()
        stats.add_stat(team_id, "foul", quarter=info["quarter"], time=info["time"])
    tk.Button(root, text="Foul", font=("Arial", 12, "bold"), command=add_foul, bg="#B0A9A9").place(x=x_pos, y=480, width=100, height=80)

# PC
def setup_pc(root, get_quarter_time, team_id, x_pos):
    def add_pc():
        info = get_quarter_time()
        stats.add_stat(team_id, "pc", quarter=info["quarter"], time=info["time"])
    tk.Button(root, text="PC", font=("Arial", 12, "bold"), command=add_pc, bg="#B0A9A9").place(x=x_pos, y=580, width=100, height=80)

# Corner
def setup_corner(root, get_quarter_time, team_id, x_pos):
    def add_corner():
        info = get_quarter_time()
        stats.add_stat(team_id, "corner", quarter=info["quarter"], time=info["time"])
    tk.Button(root, text="Corner", font=("Arial", 12, "bold"), command=add_corner, bg="#B0A9A9").place(x=x_pos, y=680, width=100, height=80)
