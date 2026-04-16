import tkinter as tk

from session import save_match_id

def setup_timer(root):
    #Quarter frame
    quarters = ["1st", "2nd", "3rd", "4th"]
    current_quarter = [0]
    
    quarter_frame = tk.Frame(root, highlightbackground="black",
            highlightthickness=2, bg="#ffffff")
    quarter_frame.place(x=600, y=90, width=300, height=50)
    quarter_label = tk.Label(
            quarter_frame,
            text=quarters[0],
            font=("Arial", 18, "bold"),
            fg="black",
            bg="#ffffff"
    )
    quarter_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    #Timer frame
    time_frame = tk.Frame(root, highlightbackground="black",
        highlightthickness=2, bg="#ffffff")
    time_frame.place(x=600, y=130, width=300, height=80)
    time_label = tk.Label(
            time_frame,
            text="00:10",
            font=("Arial", 18, "bold"),
            fg="black",
            bg="#ffffff"
    )
    time_label.place(relx=0.3, rely=0.5, anchor=tk.CENTER)

    #Adjust timer
    up_btn = tk.Button(time_frame, text="▲", font=("Arial", 12), bg="#F57E7E", command=lambda: adjust_time(1))
    down_btn = tk.Button(time_frame, text="▼", font=("Arial", 12), bg="#F57E7E", command=lambda: adjust_time(-1))
    up_btn.place(relx=0.30, rely=0.2, anchor=tk.CENTER, height=20, width=20)
    down_btn.place(relx=0.30, rely=0.8, anchor=tk.CENTER, height=20, width=20)
    up_btn.place_forget()  # Hide initially
    down_btn.place_forget()  # Hide initially

    def adjust_time(delta):
        seconds[0] = max(0, seconds[0] + delta)
        mins, secs = divmod(seconds[0], 60)
        time_label.config(text=f"{mins:02d}:{secs:02d}")
    
    def toggle_adjust_buttons(event):
        if up_btn.winfo_ismapped():
            up_btn.place_forget()
            down_btn.place_forget()
        else:
            up_btn.place(relx=0.30, rely=0.2, anchor=tk.CENTER, height=20, width=20)
            down_btn.place(relx=0.30, rely=0.8, anchor=tk.CENTER, height=20, width=20)
            root.bind("<Up>", lambda event: adjust_time(1)) # Arrow keys to adjust time
            root.bind("<Down>", lambda event: adjust_time(-1)) # Arrow keys to adjust time
    
    time_label.bind("<Button-1>", toggle_adjust_buttons)  # Show buttons on click


    seconds = [10]
    running = [False]
    finished = [False]
    job = [None]

    #Update timer function
    def update_timer():
        if running[0] and seconds[0] > 0:
            seconds[0] -= 1
            mins, secs = divmod(seconds[0], 60)
            time_label.config(text=f"{mins:02d}:{secs:02d}")
            job[0] = root.after(1000, update_timer)
        elif seconds[0] == 0:
            time_label.config(text="00:00")
            running[0] = False
            finished[0] = True
            start.config(text="Reset")
            if current_quarter[0] < len(quarters) - 1:
                current_quarter[0] += 1
                quarter_label.config(text=quarters[current_quarter[0]])
            else:
                start.config(text="Ended")
                start.config(state="disabled")
                tk.Label(root, text="Match ended", font=("Arial", 24, "bold"), fg="red").place(x=650, y=250)
                
                #Save match
                import game_state as gs
                if gs.selected_event[0] is None or gs.selected_event[0].get("event") != "pc":
                    popup = tk.Toplevel(root)
                    popup.title("Match Ended")
                    popup.geometry("300x200")
                    popup.resizable(False, False)
                    popup.grab_set()
                    popup.update_idletasks()
                    x = (popup.winfo_screenwidth() // 2) - 150
                    y = (popup.winfo_screenheight() // 2) - 100
                    popup.geometry(f"300x200+{x}+{y}")

                    tk.Label(popup, text="Match has ended", font=("Arial", 14, "bold")).pack(pady=20)

                    def on_save():
                        try:
                            from database import supabase
                            import session as ss
                            match_id = ss.get_match_id()
                            if match_id:
                                supabase.table("matches").update({"status": "finished"}).eq("id", match_id).execute()
                                print("Match saved successfully")
                        except Exception as e:
                            print(f"Error saving match: {e}")
                        popup.destroy()
                    
                    def on_new_match():
                        on_save()
                        import subprocess, sys
                        root.destroy()
                        subprocess.Popen([sys.executable, "team_data.py"])

                    tk.Button(popup, text="Save Match", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white",
                        command=on_save).pack(pady=5, fill="x", padx=20)
                    tk.Button(popup, text="Save & New Match", font=("Arial", 12, "bold"), bg="#1d3557", fg="white",
                        command=on_new_match).pack(pady=5, fill="x", padx=20)

    
    #Start/Stop/Reset button function
    def toggle_timer():
        if not running[0] and not finished[0]:
             running[0] = True
             start.config(text="Stop")
             update_timer()
        elif running[0]:
            running[0] = False
            if job[0]:
                root.after_cancel(job[0])
            start.config(text="Start")
        elif finished[0]:
            running[0] = False
            finished[0] = False
            if job[0]:
                root.after_cancel(job[0])
            seconds[0] = 10
            time_label.config(text="00:10")
            start.config(text="Start")

    #Get quarter and time
    def get_quarter_time():
        secs = seconds[0] // 60
        min = seconds[0] % 60
        return {
            "quarter": quarters[current_quarter[0]],
            "time": f"{secs:02d}:{min:02d}"
        }

    start = tk.Button(root, text="Start", font=("Arial", 12, "bold"), bg="#B0A9A9", command=toggle_timer)
    start.place(x=770, y=145, width=100, height=50) #Start button

    root.bind("<space>", lambda event: toggle_timer()) #Spacebar to start/stop/reset

    return get_quarter_time