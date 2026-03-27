import tkinter as tk

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
            text="1:00",
            font=("Arial", 18, "bold"),
            fg="black",
            bg="#ffffff"
    )
    time_label.place(relx=0.3, rely=0.55, anchor=tk.CENTER)

    seconds = [1 * 60]
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
            seconds[0] = 1 * 60
            time_label.config(text="01:00")
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
    start.place(x=770, y=148, width=100, height=50) #Start button

    return get_quarter_time