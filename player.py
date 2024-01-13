import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3

class AddPlayerForm:
    def __init__(self, root):
        self.root = root
        self.root.title("Add/Remove Player Form")

        # Frame to hold player information
        self.info_frame = ttk.LabelFrame(root, text="Player Information")
        self.info_frame.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # Fetch teams data from the database
        self.teams_data = self.get_teams_data()

        # Labels and entry fields for player information
        tk.Label(self.info_frame, text="Player Name:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.player_name = tk.Entry(self.info_frame)
        self.player_name.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        tk.Label(self.info_frame, text="Jersey Number:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.jersey_number = tk.Spinbox(self.info_frame, from_=0, to=99)
        self.jersey_number.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        tk.Label(self.info_frame, text="Height (m):").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.height = tk.Entry(self.info_frame)
        self.height.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        tk.Label(self.info_frame, text="Team:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        # Dropdown menu for showing teams using Combobox
        self.team_id = tk.StringVar(root)
        self.team_combobox = ttk.Combobox(self.info_frame, textvariable=self.team_id, state='readonly')
        self.team_combobox['values'] = [team[0] for team in self.teams_data]
        self.team_combobox.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        # Button to add player to the database
        self.add_button = tk.Button(root, text="Add Player", command=self.add_player)
        self.add_button.grid(row=4, column=0, padx=10, pady=10)

        # Button to remove player from the database
        self.remove_button = tk.Button(root, text="Remove Player", command=self.remove_player)
        self.remove_button.grid(row=5, column=0, padx=10, pady=10)


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

    def add_player(self):
        try:
            # Connect to the database
            conn = sqlite3.connect('project_db.db')
            c = conn.cursor()

            # Fetch values from entry fields
            player_name = self.player_name.get()
            jersey_number = int(self.jersey_number.get())
            height = float(self.height.get())
            team_id = self.get_selected_team_id()
            print(team_id)

            # Get the last id_player from the database
            c.execute("SELECT MAX(id_player) FROM ΠΑΙΚΤΗΣ")
            last_id = c.fetchone()[0]
            
            # If there are no players in the table yet, start from 1
            if last_id is None:
                last_id = 0

            new_id = last_id + 1  # Increment the last id by 1

            # Execute INSERT INTO query to add player with the new id
            c.execute('''
                INSERT INTO ΠΑΙΚΤΗΣ (id_player, Ονοματεπώνυμο, "Αριθμός Φανέλας", Ύψος, id_team)
                VALUES (?, ?, ?, ?, ?)
            ''', (new_id, player_name, jersey_number, height, team_id))

            # Commit changes
            conn.commit()
            print("Player added successfully!")
            # Show success message
            messagebox.showinfo("Success", "Player added successfully!")

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

    def remove_player(self):
        try:
            # Connect to the database
            conn = sqlite3.connect('project_db.db')
            c = conn.cursor()

            # Fetch values from entry fields
            player_name = self.player_name.get()
            jersey_number = int(self.jersey_number.get())

            # Execute DELETE query to remove player based on name and jersey number
            c.execute('''
                DELETE FROM ΠΑΙΚΤΗΣ
                WHERE Ονοματεπώνυμο = ? AND "Αριθμός Φανέλας" = ?
            ''', (player_name, jersey_number))

            conn.commit()
            print("Player removed successfully!")
            messagebox.showinfo("Success", "Player removed successfully!")

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
