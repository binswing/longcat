import tkinter as tk       
from tkinter import font as tkfont 
from tkinter import messagebox as msgbox
import threading
from src.play import *
from pynput import keyboard
import time
import json

class leaderboard_gui_class(tk.Frame):
    def __init__(self, parent, controller):
        self.CANVA_SIZE = 890
        self.box_arr=[]
        self.select_box_arr=[]
        self.select_box=[0,0]
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.instruction_label = tk.Canvas(self,width=745, height = 110, bg = "#43766C",highlightthickness=0)
        self.instruction_label.create_text(370,50,fill="black", font=("Comfortaa","50","bold"), text="LEADERBOARD")
        self.back_button = tk.Button(self,text='Back',height = 4, width= 10,command= lambda: self.back_cmd(), bg = "#F8FAE5",fg="#76453B",borderwidth=0)
        self.show_button = tk.Button(self,text='Show',height = 4, width= 10,command= lambda: self.show_cmd(), bg = "#F8FAE5",fg="#76453B",borderwidth=0, disabledforeground="#F2F1EB")
        self.display = tk.Canvas(self,width=1035, height = 890, bg = "#f1f1f0",highlightthickness=0)
        
        self.back_button['font'] = tkfont.Font(family="Helvetica",size=15,weight="bold")
        self.show_button['font'] = tkfont.Font(family="Helvetica",size=15,weight="bold")

        self.back_button.grid(row = 0, column = 0, sticky = "nsew" ,pady = 10,padx=10)
        self.show_button.grid(row = 0, column = 1,sticky = "nsew",pady = 10,padx=10)   
        self.instruction_label.grid(row = 0, column = 2,sticky = "nsew" ,pady = 10,padx=10)
        self.display.grid(row = 1, column = 0,columnspan=3, sticky = "nsew" ,pady = 10,padx=10)

    def show_cmd(self):
        self.show_button["state"]="disable"
        self.box_arr=[]

        name_dict = {"Rank":{"Time":"Time","Name":"Name"}}

        with open("./src/lib/leaderboard.json","r") as f:
            leaderboard = json.load(f)
        leaderboard_key = leaderboard.keys()
        if leaderboard_key is not None:
            leaderboard_key = sorted([int(i) for i in leaderboard_key])
            index = 1
            for key in leaderboard_key:
                second = str(key % 60)
                minute = str(int((key - key % 60)/60))
                while len(second) < 2: second = "0" + second
                while len(minute) < 2: minute = "0" + minute
                for name in leaderboard[str(key)]:
                    if index > 20: break
                    name_dict[str(index)] = {"Time":minute+":"+second,"Name":name}
                    index+=1
            
            height=index
            box_height = 42

            for i in range(height):
                self.display.create_rectangle(0,i*box_height,1035,(i+1)*box_height,outline="",fill="#F2FFE9")
            
            for i in range(height):
                self.display.create_line(0,i*box_height,1035,i*box_height,fill="black")
            self.display.create_line(0,height*box_height-1,1035,height*box_height-1,fill="black")

            self.display.create_line(0,0,0,height*box_height,fill="black")
            self.display.create_line(135,0,135,height*box_height,fill="black")
            self.display.create_line(435,0,435,height*box_height,fill="black")
            self.display.create_line(1034,0,1034,height*box_height,fill="black")
            line = 0
            for rank in name_dict.keys():
                self.display.create_text(65, (2*line+1)*box_height/2, text=rank, fill="black", font=('Helvetica 15 bold'))
                self.display.create_text(285, (2*line+1)*box_height/2, text=name_dict[rank]["Time"], fill="black", font=('Helvetica 15 bold'))
                self.display.create_text(735, (2*line+1)*box_height/2, text=name_dict[rank]["Name"], fill="black", font=('Helvetica 15 bold'))
                line+=1

    def reset_frame(self):
        self.display.delete("all")
        self.show_button["state"]="normal"

    def back_cmd(self):
        self.reset_frame()
        self.controller.show_frame("lobby_gui_class")