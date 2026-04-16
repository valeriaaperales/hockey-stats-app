import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sys
import os
import json
from database import supabase
import session as ss

def main():
    root = tk.Tk()
    root.title("Teams and players")
    root.state("zoomed")

    columns = ("No", "First Name", "Last Name", "Position", "Starter")

    # Team 1
    tk.Label(root, text="Team 1  - ", font=("Arial", 18, "bold")).place(x=70, y=50)
    team1_entry = tk.Entry(root, font=("Arial", 18))
    team1_entry.place(x=200, y=50, width=300)

    canvas1 = tk.Canvas(root, width=70, height=45, bg="#DDDDDD", highlightthickness=1, highlightbackground="#999")
    canvas1.place(x=515, y=50)
    select1 = ttk.Combobox(root, values=["Red", "Blue", "Green", "Yellow", "Black", "White"], state="readonly")
    select1.place(x=500, y=100, width=100)
    select1.set("Select Color...")

    table1 = ttk.Treeview(root, columns=columns, show="headings", height=25)
    for col in columns:
        table1.heading(col, text=col)
        table1.column(col, width=80, anchor="center")
    table1.place(x=70, y=170, width=450)
    table1.tag_configure("odd", background="#c9c9c9")
    table1.tag_configure("even", background="#e2e2e2")

    for i in range(8):
        tag = "even" if i % 2 == 0 else "odd"
        table1.insert("", "end", values=("", "", "", "", ""), tags=(tag,))

    def add_player1():
        count = len(table1.get_children())
        tag = "even" if count % 2 == 0 else "odd"
        table1.insert("", "end", values=("", "", "", "", ""), tags=(tag,))

    def remove_player1():
        selected = table1.selection()
        if selected:
            table1.delete(selected[0])

    # Team 2
    tk.Label(root, text="Team 2  - ", font=("Arial", 18, "bold")).place(x=900, y=50)
    team2_entry = tk.Entry(root, font=("Arial", 18))
    team2_entry.place(x=1030, y=50, width=300)

    canvas2 = tk.Canvas(root, width=70, height=45, bg="#DDDDDD", highlightthickness=1, highlightbackground="#999")
    canvas2.place(x=1348, y=50)
    select2 = ttk.Combobox(root, values=["Red", "Blue", "Green", "Yellow", "Black", "White"], state="readonly")
    select2.place(x=1333, y=100, width=100)
    select2.set("Select Color...")

    table2 = ttk.Treeview(root, columns=columns, show="headings", height=25)
    for col in columns:
        table2.heading(col, text=col)
        table2.column(col, width=80, anchor="center")
    table2.place(x=900, y=170, width=450)
    table2.tag_configure("odd", background="#c9c9c9")
    table2.tag_configure("even", background="#e2e2e2")

    for i in range(8):
        tag = "even" if i % 2 == 0 else "odd"
        table2.insert("", "end", values=("", "", "", "", ""), tags=(tag,))

    def add_player2():
        count = len(table2.get_children())
        tag = "even" if count % 2 == 0 else "odd"
        table2.insert("", "end", values=("", "", "", "", ""), tags=(tag,))

    def remove_player2():
        selected = table2.selection()
        if selected:
            table2.delete(selected[0])

    # Edit cell
    def edit_cell(event, table, offset_x, offset_y):
        data = table.identify_row(event.y)
        column = table.identify_column(event.x)
        if not data or not column:
            return
        column_index = int(column.replace("#", "")) - 1
        x, y, width, height = table.bbox(data, column)
        value = table.item(data, "values")[column_index]

        if column_index == 4:  # Starter column
            current_values = list(table.item(data, "values"))
            current_values[4] = "No" if value == "Yes" else "Yes"
            table.item(data, values=current_values)
        else:
            def validate_input(char, col_index):
                if col_index == 0:  #Only numbers for the No column
                    return char.isdigit()
                else:  # Only letters for the First Name and Last Name columns
                    return char.isalpha() or char == ""

            vcmd = (root.register(lambda P, col=column_index: validate_input(P, col)), '%S')
            entry = tk.Entry(root, font=("Arial", 10), validate="key", validatecommand=vcmd)
            entry.place(x=x + offset_x, y=y + offset_y, width=width, height=height)
            entry.insert(0, value)
            entry.focus()
            def capitalize_entry(event):
                text = entry.get()
                entry.delete(0, tk.END)
                entry.insert(0, text.upper())
            entry.bind("<KeyRelease>", capitalize_entry)
            def save_edit(event=None):
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
        colors = ["Red", "Blue", "Green", "Yellow", "Black", "White"]
        colors_hex = {
            "Red": "#FF0000", "Blue": "#0000FF", "Green": "#00AA00",
            "Yellow": "#FFD700", "Black": "#000000", "White": "#FFFFFF"
        }
        color1 = select1.get()
        color2 = select2.get()
        if color1 in colors_hex:
            canvas1.configure(bg=colors_hex[color1])
        if color2 in colors_hex:
            canvas2.configure(bg=colors_hex[color2])

        #Update color options to prevent selecting the same color for both teams
        if color1 in colors:
            select2.config(values=[c for c in colors if c != color1])
        else:
            select2.config(values=colors)

        #Reset if color selected is not available anymore
        if color1 == color2:
            select2.set("Select Color...")
            canvas2.configure(bg="#DDDDDD")

    select1.bind("<<ComboboxSelected>>", lambda event: show_color())
    select2.bind("<<ComboboxSelected>>", lambda event: show_color())

    #Capitalize team names
    def capitalize_team1(event):
        team = team1_entry.get()
        team1_entry.delete(0, tk.END)
        team1_entry.insert(0, team.upper())

    def capitalize_team2(event):
        team = team2_entry.get()
        team2_entry.delete(0, tk.END)
        team2_entry.insert(0, team.upper())

    vcmd_alpha = (root.register(lambda P: P.isalpha() or P == " "), '%S') #Only letters and spaces for team names
    team1_entry.config(validate="key", validatecommand=vcmd_alpha)
    team2_entry.config(validate="key", validatecommand=vcmd_alpha)
    team1_entry.bind("<KeyRelease>", capitalize_team1)
    team2_entry.bind("<KeyRelease>", capitalize_team2)

    # Save teams
    def save_teams():
        if not team1_entry.get().strip():
            messagebox.showwarning("Warning", "Please enter a name for Team 1.")
            return
        if not team2_entry.get().strip():
            messagebox.showwarning("Warning", "Please enter a name for Team 2.")
            return
        if select1.get() == "Select Color...":
            messagebox.showwarning("Warning", "Please select a color for Team 1.")
            return
        if select2.get() == "Select Color...":
            messagebox.showwarning("Warning", "Please select a color for Team 2.")
            return
        players1 = [list(table1.item(i, "values")) for i in table1.get_children()]
        players2 = [list(table2.item(i, "values")) for i in table2.get_children()]
        valid_players1 = [p for p in players1 if p[0] and p[1] and p[2]]
        valid_players2 = [p for p in players2 if p[0] and p[1] and p[2]]
        if len(valid_players1) < 8:
            messagebox.showwarning("Warning", "Team 1 must have at least 8 players with number, first name and last name valid.")
            return
        if len(valid_players2) < 8:
            messagebox.showwarning("Warning", "Team 2 must have at least 8 players with number, first name and last name valid.")
            return
        
        # Save data to JSON
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

        # Insert teams in Supabase
        try:
            def upsert_team(name, color):
                existing = supabase.table("teams").select("id").eq("name", name).execute()
                if existing.data:
                    team_id = existing.data[0]["id"]
                    supabase.table("teams").update({"color": color}).eq("id", team_id).execute()
                else:
                    response = supabase.table("teams").insert({"name": name, "color": color}).execute()
                    team_id = response.data[0]["id"]
                return team_id

            def upsert_player(team_id, p):
                existing = supabase.table("players").select("id").eq("team_id", team_id).eq("number", int(p[0])).execute()
                if existing.data:
                    supabase.table("players").update({
                        "first_name": p[1],
                        "last_name": p[2],
                        "position": p[3],
                        "starter": p[4] == "Yes"
                    }).eq("id", existing.data[0]["id"]).execute()
                else:
                    supabase.table("players").insert({
                        "team_id": team_id,
                        "number": int(p[0]),
                        "first_name": p[1],
                        "last_name": p[2],
                        "position": p[3],
                        "starter": p[4] == "Yes"
                    }).execute()

            team1_id = upsert_team(team1_entry.get(), select1.get())
            team2_id = upsert_team(team2_entry.get(), select2.get())

            for p in valid_players1:
                upsert_player(team1_id, p)

            for p in valid_players2:
                upsert_player(team2_id, p)

            ss.save_teams_ids(team1_id, team2_id)

            # Create match in Supabase
            match_response = supabase.table("matches").insert({
                "team1_id": team1_id,
                "team2_id": team2_id,
                "team1_score": 0,
                "team2_score": 0,
                "status": "live"
            }).execute()

            match_id = match_response.data[0]["id"]
            ss.save_match_id(match_id)


        except Exception as e:
            print(f"Error saving to database: {e}")
            messagebox.showwarning("Warning", "Could not connect to Supabase. Data saved locally only.")
            
        root.destroy()
        subprocess.Popen([sys.executable, "main.py"])

    # Buttons
    tk.Button(root, text="Add Player", font=("Arial", 10, "bold"), bg="#66B9F0", command=add_player1).place(x=525, y=600, width=105, height=46)
    tk.Button(root, text="Remove Player", font=("Arial", 10, "bold"), bg="#F17272", command=remove_player1).place(x=525, y=650, width=105, height=46)
    tk.Button(root, text="Add Player", font=("Arial", 10, "bold"), bg="#66B9F0", command=add_player2).place(x=1355, y=600, width=105, height=46)
    tk.Button(root, text="Remove Player", font=("Arial", 10, "bold"), bg="#F17272", command=remove_player2).place(x=1355, y=650, width=105, height=46)
    tk.Button(root, text="Save Teams", font=("Arial", 10, "bold"), bg="#8FE268", command=save_teams).place(x=660, y=720, width=120, height=70)

    root.mainloop()

if __name__ == "__main__":
    main()