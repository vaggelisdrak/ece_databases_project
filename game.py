import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3

class AddPlayerForm:
    def __init__(self, root):
        self.root = root
        self.root.title("Add/Remove Game Form")

        # Frame to hold player information
        self.info_frame = ttk.LabelFrame(root, text="Game Information")
        self.info_frame.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # Fetch teams data from the database
        self.teams_data = self.get_teams_data()

        # Labels and entry fields for player information
        tk.Label(self.info_frame, text="Date (m/d/y):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.date = tk.Entry(self.info_frame)
        self.date.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        # Labels and entry fields for player information
        tk.Label(self.info_frame, text="Game Type:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.game_type = tk.Entry(self.info_frame)
        self.game_type.insert(0, "REGULAR SEASON")
        self.game_type.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        tk.Label(self.info_frame, text="Winner:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        # Dropdown menu for teams using Combobox
        self.team1_id = tk.StringVar(root)
        self.team1_combobox = ttk.Combobox(self.info_frame, textvariable=self.team1_id, state='readonly')
        self.team1_combobox['values'] = [team[0] for team in self.teams_data]
        self.team1_combobox.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        tk.Label(self.info_frame, text="Loser:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        # Dropdown menu for teams using Combobox
        self.team2_id = tk.StringVar(root)
        self.team2_combobox = ttk.Combobox(self.info_frame, textvariable=self.team2_id, state='readonly')
        self.team2_combobox['values'] = [team[0] for team in self.teams_data]
        self.team2_combobox.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        # 

        # Button to add player to the database
        self.add_button = tk.Button(root, text="Add Game", command=self.add_game)
        self.add_button.grid(row=4, column=0, padx=10, pady=10)



    def get_teams_data(self):
        try:
            # Connect to the database
            conn = sqlite3.connect('project_db.db')
            c = conn.cursor()

            # Fetch teams data
            c.execute("SELECT Όνομα, id_team FROM ΟΜΑΔΑ")
            teams = c.fetchall()
            print(teams)

            return teams

        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return []

        finally:
            # Close the connection
            if conn:
                conn.close()

    def get_selected_team_id(self):
        # Find the selected team's ID
        selected_team_name = self.team_id.get()
        print(selected_team_name)
        print('teams data', self.teams_data)
        for team in self.teams_data:
            if team[0] == selected_team_name:
                return team[1]
        return None

    def add_game(self):
        try:
            # Connect to the database
            conn = sqlite3.connect('project_db.db')
            c = conn.cursor()

            # Fetch values from entry fields
            date = self.date.get()  # Fetch the date from the entry field
            game_type = self.game_type.get()
            team1 = self.team1_id.get()
            team2 = self.team2_id.get()

            # Get the last id_player from the database
            c.execute("SELECT MAX(id_game) FROM ΑΓΩΝΑΣ")
            last_id = c.fetchone()[0]
            
            # If there are no players in the table yet, start from 1
            if last_id is None:
                last_id = 0

            new_id = last_id + 1  # Increment the last id by 1

            knock_out_game = 0
            if game_type != 'REGULAR SEASON':
                knock_out_game = 1

            # Execute INSERT INTO query to add player with the new id
            c.execute('''
                INSERT INTO ΑΓΩΝΑΣ (Νικητής, Ηττημένος, Ημερομηνία, "KNOCK OUT GAME", Είδος, id_game)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (team1, team2, date, knock_out_game, game_type ,new_id))

            # Commit changes
            conn.commit()
            print("Game added successfully!")
            # Show success message
            messagebox.showinfo("Success", "Game added successfully!")

        except sqlite3.Error as e:
            # Show error message for database-related errors
            messagebox.showerror("Database Error", f"An error occurred: {e}")

        except Exception as ex:
            # Show error message for other exceptions
            messagebox.showerror("Error", f"An unexpected error occurred: {ex}")

        finally:
            # Close the connection
            if conn:
                conn.close()
        

# Create the Tkinter window
root = tk.Tk()
app = AddPlayerForm(root)
root.mainloop()
