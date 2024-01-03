from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk,Image 
import sqlite3
import time

class Loadingscreen():
    '''loading bar'''
    def __init__(self,root):
        self.root=root

        self.img = ImageTk.PhotoImage(Image.open("basketball_bg.jpg"))#---background img
        self.bg = Label(self.root,image=self.img)
        self.bg.place(x=0,y=0,relwidth=1,relheight=1)

        self.fr = Frame(self.bg)
        self.fr.pack(expand=True)

        self.txt = Label(self.fr,text='loading...',font='none 12 bold')
        self.txt.grid(row=0,column=0,pady=10)

        self.progress_var = StringVar()
        self.loading = ttk.Progressbar(self.fr ,variable =self.progress_var, orient=HORIZONTAL, length=400, mode='determinate')
        self.loading.grid(row=1,column=0)

        self.calculation()

    def progress(self):#---animation
        for x in range(101):   
            time.sleep(0.02)
            self.txt["text"]='loading...'+str(x)+' %'
            self.progress_var.set(x)
            self.bg.update()
        if x==100:
            self.root.forget()

    def calculation(self):#---avoid errors
        try:
            self.progress()
        except:
            pass

class GUI():
    def __init__(self, root):
        self.root = root

        self.widget = Frame(self.root, bg='#333', bd=5)
        self.widget.pack(fill='both', expand=1)

        self.menu = Frame(self.widget, bg='#333', bd=5)
        self.menu.pack(side='top', fill='x')

        # Create four buttons on top of each other within the 'widget' frame
        button_texts = ['ΑΓΩΝΕΣ', 'ΒΑΘΜΟΛΟΓΙΕΣ', 'ΟΜΑΔΕΣ', 'ΣΤΑΤΙΣΤΙΚΑ']
        for text in button_texts:
            button = Button(self.menu, text=text, height=4, font='ariel 15 bold', command=lambda t=text: self.show_window(t))
            button.pack(side='left', padx=5, pady=5, fill='x', expand=1)

        self.label = Label(self.widget, text="", font='ariel 15 bold', bg='#333', fg='white')
        self.label.pack(fill='x')

    def show_window(self, text):
        self.label.config(text=text)
        if text == 'ΑΓΩΝΕΣ':
            self.show_games()
        if text == 'ΒΑΘΜΟΛΟΓΙΕΣ':
            self.show_standings()
        if text == 'ΟΜΑΔΕΣ':
            self.show_teams()
        if text == 'ΣΤΑΤΙΣΤΙΚΑ':
            self.show_stats()

    def show_games(self):
        # Connect to the SQLite database
        connection = sqlite3.connect('project_db.db')
        cursor = connection.cursor()

        # Your SQL query
        sql_query = """
        SELECT a.Ημερομηνία, a.Είδος, p.'HOME TEAM', p.'AWAY TEAM ', p.Γήπεδο, p.'Points ΗΟΜΕ', p.'Points AWAY'
        FROM ΑΓΩΝΑΣ AS a, Παίζει AS p
        WHERE a.id_game = p.id_game
        GROUP BY a.id_game
        ORDER BY a.Ημερομηνία
        """

        # Execute the query
        cursor.execute(sql_query)
        games_data = cursor.fetchall()  # Fetch all results

        print(games_data)

        # Close the connection
        connection.close()
        
        # Remove the old text widgets if they exist
        if hasattr(self, 'text_widget'):
            self.text_widget.destroy()
        if hasattr(self, 'text_widget1'):
            self.text_widget1.destroy()
        if hasattr(self, 'text_widget2'):
            self.text_widget2.destroy()
        if hasattr(self, 'frame'):
            self.frame.destroy()

        # Create a new frame widget
        self.frame = Frame(self.widget)
        self.frame.pack()


        # Create two new text widgets
        self.text_widget1 = Text(self.frame, width=50, height=30, bg='#333', fg='white', font=('Arial', 12))
        self.text_widget2 = Text(self.frame, width=50, height=30, bg='#333', fg='white', font=('Arial', 12))

        # Place the text widgets in the frame using a grid layout
        self.text_widget1.grid(row=0, column=0)
        self.text_widget2.grid(row=0, column=1)

        for i, row in enumerate(games_data):
            if row[1] == 'REGULAR SEASON':
                new_row = row[:1] + row[2:4] + row[5:]  # Create a new tuple without the second and fifth elements
                row_str = f" {new_row[0]}\n {new_row[1]}\t\t{new_row[3]}\n {new_row[2]}\t\t{new_row[4]}\n"
            else:
                row_str = ', '.join(map(str, row))

            # Insert the row into the first text widget if i is even, otherwise insert it into the second text widget
            if i % 2 == 0:
                self.text_widget1.insert('end', row_str + '\n')
            else:
                self.text_widget2.insert('end', row_str + '\n')

    def show_teams(self):
        # Connect to the SQLite database and fetch teams data
        connection = sqlite3.connect('project_db.db')
        cursor = connection.cursor()

        # Your SQL query
        sql_query = """
        SELECT om.Όνομα AS "ΟΜΑΔΑ", p.Ονοματεπώνυμο
        FROM ΟΜΑΔΑ AS om
        LEFT JOIN ΠΑΙΚΤΗΣ AS p
        ON om.id_team = p.id_team
        """

        cursor.execute('CREATE INDEX idx_show_teams ON ΟΜΑΔΑ(id_team)')

        # Query without an index
        start_time = time.time()
        
        # Execute the query
        cursor.execute(sql_query)
        
        teams_data = cursor.fetchall()  # Fetch all results

        #print(teams_data)

        end_time = time.time()
        execution_time_without_index = end_time - start_time
        print(f"Execution time without index: {execution_time_without_index} seconds")

        # Close the connection
        connection.close()
        
        # Remove the old text widgets if they exist
        if hasattr(self, 'text_widget'):
            self.text_widget.destroy()
        if hasattr(self, 'text_widget1'):
            self.text_widget1.destroy()
        if hasattr(self, 'text_widget2'):
            self.text_widget2.destroy()
        if hasattr(self, 'frame'):
            self.frame.destroy()

        # Create a new frame widget
        self.frame = Frame(self.widget)
        self.frame.pack()

        team_widgets = {}  # Create an empty dictionary to store the text widgets for each team
        team_count = 0  # Initialize a counter for the number of teams

        for row in teams_data:
            team_name = row[0]  # Get the team name
            team_player = row[1]  # Get the player name

            # If the team name is not in the dictionary, create a new text widget for it
            if team_name not in team_widgets:
                text_widget = Text(self.frame, width=25, height=11, bg='#333', fg='white', font=('Arial', 12))
                text_widget.grid(row=team_count // 6, column=team_count % 6)  # Place the text widget in the appropriate row and column
                text_widget.tag_configure("bold", font=("Arial", 14, "bold"))
                text_widget.insert('end', ' ' + team_name + '\n\n', "bold")
                team_widgets[team_name] = text_widget  # Add the text widget to the dictionary
                team_count += 1  # Increment the counter for the number of teams

            # Insert the player name into the text widget for the team
            team_widgets[team_name].insert('end', ' '+ team_player + '\n')
        
            # New code to fill remaining cells with gray widgets
            rows = team_count // 6
            if team_count % 6 != 0:  # If there are any teams in the last row
                rows += 1  # Add one to the number of rows

            for i in range(team_count, rows * 6):  # For each remaining cell in the grid
                text_widget = Text(self.frame, width=25, height=11, bg='#333', fg='white', font=('Arial', 12))  # Create a gray text widget
                text_widget.grid(row=i // 6, column=i % 6)  # Place the text widget in the appropriate row and column
                    
    def show_standings(self):
        
        # Connect to the SQLite database
        connection = sqlite3.connect('project_db.db')
        cursor = connection.cursor()

        # Your SQL query
        sql_query_east = """
        SELECT team, SUM(win) AS Wins, SUM(loss) AS Losses 
        FROM (
            SELECT Νικητής AS team, COUNT(*) AS win, 0 AS loss, 'Όνομα', id_group
            FROM ΑΓΩΝΑΣ, ΟΜΑΔΑ
            WHERE ΟΜΑΔΑ.'Όνομα' = Νικητής AND ΟΜΑΔΑ.id_group = 1
            GROUP BY Νικητής
            UNION ALL
            SELECT Ηττημένος AS team, 0 AS win, COUNT(*) AS loss, 'Όνομα', id_group
            FROM ΑΓΩΝΑΣ, ΟΜΑΔΑ
            WHERE ΟΜΑΔΑ.'Όνομα' = Ηττημένος AND ΟΜΑΔΑ.id_group = 1
            GROUP BY Ηττημένος
        ) 
        GROUP BY team
        ORDER BY Wins DESC
        """
        sql_query_west = """
        SELECT team, SUM(win) AS Wins, SUM(loss) AS Losses 
        FROM (
            SELECT Νικητής AS team, COUNT(*) AS win, 0 AS loss, 'Όνομα', id_group
            FROM ΑΓΩΝΑΣ, ΟΜΑΔΑ
            WHERE ΟΜΑΔΑ.'Όνομα' = Νικητής AND ΟΜΑΔΑ.id_group = 2
            GROUP BY Νικητής
            UNION ALL
            SELECT Ηττημένος AS team, 0 AS win, COUNT(*) AS loss, 'Όνομα', id_group
            FROM ΑΓΩΝΑΣ, ΟΜΑΔΑ
            WHERE ΟΜΑΔΑ.'Όνομα' = Ηττημένος AND ΟΜΑΔΑ.id_group = 2
            GROUP BY Ηττημένος
        ) 
        GROUP BY team
        ORDER BY Wins DESC
        """

        # Execute the query
        cursor.execute(sql_query_east)
        east_data = cursor.fetchall()  # Fetch all results
        
        cursor.execute(sql_query_west)
        west_data = cursor.fetchall()  # Fetch all results

        print(east_data)
        print(west_data)

        # Close the connection
        connection.close()
        
         # Remove the old text widget if it exists
        if hasattr(self, 'text_widget'):
            self.text_widget.destroy()
        if hasattr(self, 'text_widget1'):
            self.text_widget1.destroy()
        if hasattr(self, 'text_widget2'):
            self.text_widget2.destroy()
        if hasattr(self, 'frame'):
            self.frame.destroy()
            
        # Create a new frame widget
        self.frame = Frame(self.widget)
        self.frame.pack()
            
        # Create two new text widgets
        self.text_widget1 = Text(self.frame, width=50, height=30, bg='#333', fg='white', font=('Arial', 12))
        self.text_widget2 = Text(self.frame, width=50, height=30, bg='#333', fg='white', font=('Arial', 12))

        # Place the text widgets in the frame using a grid layout
        self.text_widget1.grid(row=0, column=0)
        self.text_widget2.grid(row=0, column=1)
        
        self.text_widget1.tag_configure("bold", font=("Arial", 14, "bold"))
        self.text_widget2.tag_configure("bold", font=("Arial", 14, "bold"))

        self.text_widget1.insert('end', '\n '+ 'EASTERN CONFERENCE' + '\n\n', "bold")
        for row in east_data:
            self.text_widget1.insert('end', ' '+ row[0] + '\t\t\t' + str(row[1]) + '-' +  str(row[2]) +'\n\n')
            

        self.text_widget2.insert('end', '\n '+ 'WESTERN CONFERENCE' + '\n\n', "bold")
        for row in west_data:
            self.text_widget2.insert('end', ' '+ row[0] + '\t\t\t' + str(row[1]) + '-' +  str(row[2]) +'\n\n')

    def show_stats(self):
        # Connect to the SQLite database and fetch teams data
        connection = sqlite3.connect('project_db.db')
        cursor = connection.cursor()
        
        # Remove the old text widgets if they exist
        if hasattr(self, 'text_widget'):
            self.text_widget.destroy()
        if hasattr(self, 'text_widget1'):
            self.text_widget1.destroy()
        if hasattr(self, 'text_widget2'):
            self.text_widget2.destroy()
        if hasattr(self, 'frame'):
            self.frame.destroy()
            
        # Create a new text widget and insert the data
        self.text_widget = Text(self.widget, width=100, height=50, bg='#333', fg='white', font=('Arial', 12))
        self.text_widget.pack()

        # Your SQL query FOR PPG ---------------------------------------------
        sql_query = """
        SELECT P.Ονοματεπώνυμο, AVG(A.Points) AS PPG
        FROM "Αγωνίζεται " AS A, ΠΑΙΚΤΗΣ AS P
        WHERE P.id_player = A.id_player
        GROUP BY A.id_player
        ORDER BY PPG DESC
        LIMIT 5
        """

        # Execute the query FOR PPG
        cursor.execute(sql_query)
        ppg_standings = cursor.fetchall()  # Fetch all results

        print(ppg_standings)
        
        self.text_widget.tag_configure("bold", font=("Arial", 14, "bold"))
        self.text_widget.insert('end', ' Points Per Game' + '\n\n', "bold")
        
        for row in ppg_standings:
            row_str = ', '.join(map(str, row))
            self.text_widget.insert('end', ' '+ row_str + '\n')

        # Your SQL query RPG --------------------------------------------------
        sql_query = """
        SELECT P.Ονοματεπώνυμο, AVG(A.Rebounds) AS RPG
        FROM "Αγωνίζεται " AS A, ΠΑΙΚΤΗΣ AS P
        WHERE P.id_player = A.id_player
        GROUP BY A.id_player
        ORDER BY RPG DESC
        LIMIT 5
        """

        # Execute the query FOR RPG
        cursor.execute(sql_query)
        rpg_standings = cursor.fetchall()  # Fetch all results

        print(rpg_standings)
        
        self.text_widget.tag_configure("bold", font=("Arial", 14, "bold"))
        self.text_widget.insert('end', '\n\n Rebounds Per Game' + '\n\n', "bold")
        
        for row in rpg_standings:
            row_str = ', '.join(map(str, row))
            self.text_widget.insert('end', ' '+ row_str + '\n')

        # Your SQL query FOR APG -------------------------------------------------
        sql_query = """
        SELECT P.Ονοματεπώνυμο, AVG(A.Assists) AS APG
        FROM "Αγωνίζεται " AS A, ΠΑΙΚΤΗΣ AS P
        WHERE P.id_player = A.id_player
        GROUP BY A.id_player
        ORDER BY APG DESC
        LIMIT 5
        """

        # Execute the query
        cursor.execute(sql_query)
        apg_standings = cursor.fetchall()  # Fetch all results

        print(apg_standings)
        
        self.text_widget.tag_configure("bold", font=("Arial", 14, "bold"))
        self.text_widget.insert('end', '\n\n Assists Per Game' + '\n\n', "bold")
        
        for row in apg_standings:
            row_str = ', '.join(map(str, row))
            self.text_widget.insert('end', ' '+ row_str + '\n')

        # Close the connection
        connection.close()


        
# main        

class Main():
    def __init__(self): 
        root = Tk()
        root.title('Basketball tournament')
        root.state('zoomed')#fullscreen
        #root.resizable(False,False)
        Loadingscreen(root)
        #-----------------------------------------
        root.title('Basketball tournament')
        root.state('zoomed')
        root.configure(background = 'black')
        #root.geometry('1915x1050')
        GUI(root)
        
        root.mainloop()

      
if __name__ == "__main__":
    Main()