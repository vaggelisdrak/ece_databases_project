from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk,Image 
import sqlite3
import re
import time
import webbrowser

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

        # Execute the query
        cursor.execute(sql_query)
        teams_data = cursor.fetchall()  # Fetch all results

        print(teams_data)

        # Close the connection
        connection.close()

    def show_standings(self):
        pass

    def show_stats(self):
        # Connect to the SQLite database and fetch teams data
        connection = sqlite3.connect('project_db.db')
        cursor = connection.cursor()

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