import tkinter as tk
from tkinter import ttk
import subprocess
import sys
import json

def main():
    root = tk.Tk()
    root.title("Teams and players")
    root.geometry("1500x800")

    columns = ("No", "First Name", "Last Name", "Starter")

    # Team 1
    tk.Label(root, text="Team 1  - ", font=("Arial", 18, "bold")).place(x=70, y=50)
    team1_entry = tk.Entry(root, font=("Arial", 18))
    team1_entry.place(x=200, y=50, width=300)

    canvas1 = tk.Canvas(root, width=70, height=45, bg="#DDDDDD", highlightthickness=1, highlightbackground="#999")
    canvas1.place(x=515, y=50)
    select1 = ttk.Combobox(root, values=["Red", "Blue", "Green", "Yellow", "Black", "White"], state="readonly")
    select1.place(x=500, y=100, width=100)
    select1.set("Select Color...")

    table1 = ttk.Treeview(root, columns=columns, show="headings", height=8)
    for col in columns:
        table1.heading(col, text=col)
        table1.column(col, width=80, anchor="center")
    table1.place(x=70, y=170, width=450)
    table1.tag_configure("odd", background="#c9c9c9")
    table1.tag_configure("even", background="#e2e2e2")

    def add_player1():
        count = len(table1.get_children())
        tag = "even" if count % 2 == 0 else "odd"
        table1.insert("", "end", values=("", "", "", ""), tags=(tag,))
    tk.Button(root, text="Add Player", font=("Arial", 10, "bold"), bg="#B0A9A9", command=add_player1).place(x=525, y=370)

    # Team 2
    tk.Label(root, text="Team 2  - ", font=("Arial", 18, "bold")).place(x=900, y=50)
    team2_entry = tk.Entry(root, font=("Arial", 18))
    team2_entry.place(x=1030, y=50, width=300)

    canvas2 = tk.Canvas(root, width=70, height=45, bg="#DDDDDD", highlightthickness=1, highlightbackground="#999")
    canvas2.place(x=1348, y=50)
    select2 = ttk.Combobox(root, values=["Red", "Blue", "Green", "Yellow", "Black", "White"], state="readonly")
    select2.place(x=1333, y=100, width=100)
    select2.set("Select Color...")

    table2 = ttk.Treeview(root, columns=columns, show="headings", height=8)
    for col in columns:
        table2.heading(col, text=col)
        table2.column(col, width=80, anchor="center")
    table2.place(x=900, y=170, width=450)
    table2.tag_configure("odd", background="#c9c9c9")
    table2.tag_configure("even", background="#e2e2e2")

    def add_player2():
        count = len(table2.get_children())
        tag = "even" if count % 2 == 0 else "odd"
        table2.insert("", "end", values=("", "", "", ""), tags=(tag,))
    tk.Button(root, text="Add Player", font=("Arial", 10, "bold"), bg="#B0A9A9", command=add_player2).place(x=1355, y=370)

    # Edit cell
    def edit_cell(event, table, offset_x, offset_y):
        data = table.identify_row(event.y)
        column = table.identify_column(event.x)
        if not data or not column:
            return
        
        column_index = int(column.replace("#", "")) - 1
        x, y, width, height = table.bbox(data, column)
        value = table.item(data, "values")[column_index]

        if column_index == 3:  # Starter column
            current_values = list(table.item(data, "values"))
            current_values[3] = "No" if value == "Yes" else "Yes"
            table.item(data, values=current_values)
        else:
            entry = tk.Entry(root, font=("Arial", 10))
        entry.place(x=x + offset_x, y=y + offset_y, width=width, height=height)
        entry.insert(0, value)
        entry.focus()
        def save_edit(event):
            new_value = entry.get()
            current_values = list(table.item(data, "values"))
            current_values[column_index] = new_value
            table.item(data, values=current_values)
            entry.destroy()
        entry.bind("<Return>", save_edit)
        entry.bind("<FocusOut>", save_edit)

    table1.bind("<Button-1>", lambda event: edit_cell(event, table1, 70, 170))
    table2.bind("<Button-1>", lambda event: edit_cell(event, table2, 900, 170))

    # Colors
    def show_color():
        color1 = select1.get()
        color2 = select2.get()
        colors_hex = {
            "Red": "#FF0000", "Blue": "#0000FF", "Green": "#00AA00",
            "Yellow": "#FFD700", "Black": "#000000", "White": "#FFFFFF"
        }
        if color1 in colors_hex:
            canvas1.configure(bg=colors_hex[color1])
        if color2 in colors_hex:
            canvas2.configure(bg=colors_hex[color2])

    select1.bind("<<ComboboxSelected>>", lambda event: show_color())
    select2.bind("<<ComboboxSelected>>", lambda event: show_color())

    # Save teams
    def save_teams():
        players1 = [list(table1.item(i, "values")) for i in table1.get_children()]
        players2 = [list(table2.item(i, "values")) for i in table2.get_children()]
        data = {
            "team1_name": team1_entry.get(),
            "team2_name": team2_entry.get(),
            "team1_color": select1.get(),
            "team2_color": select2.get(),
            "players_team1": players1,
            "players_team2": players2
        }
        with open("teams_data.json", "w") as f:
            json.dump(data, f)
        root.destroy()
        subprocess.Popen([sys.executable, "main.py"])

    tk.Button(root, text="Save Teams", font=("Arial", 10, "bold"), bg="#B0A9A9", command=save_teams).place(x=700, y=700)

    root.mainloop()

if __name__ == "__main__":
    main()