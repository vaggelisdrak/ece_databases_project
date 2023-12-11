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
    def __init__(self,root):
        self.root=root
        #------------------------------------------------------------------------------------------- main frames

        self.widget = Frame(self.root, bg='white', bd=5)
        self.widget.pack(fill='both', expand=1)


# main        

class Main():
    def __init__(self): 
        try: 
            root = Tk()
            root.title('Basketball tournament')
            root.state('zoomed')#fullscreen
            #root.resizable(False,False)
            Loadingscreen(root)
            #-----------------------------------------
            root.title('Basketball tournament')
            root.state('zoomed')
            #root.geometry('1915x1050')
            GUI(root)
            root.mainloop()
        except:
            pass
      
if __name__ == "__main__":
    Main()