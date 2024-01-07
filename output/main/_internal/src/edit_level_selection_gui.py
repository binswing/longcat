import tkinter as tk       
from tkinter import font as tkfont 
import threading
from src.head import *
from pynput import keyboard
import time
import json

class edit_level_selection_gui_class(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        self.back_button = tk.Button(self,text='BACK',height = 8, width= 12,command= lambda: self.back_cmd(), bg = "#F8FAE5",fg="#76453B",borderwidth=0)
        self.submit_button = tk.Button(self,text='SUBMIT LEVEL',height = 8, width= 15,command= lambda: self.submit_cmd(), bg = "#F8FAE5",fg="#76453B",borderwidth=0)
        self.back_button['font'] = tkfont.Font(family="Helvetica",size=20,weight="bold")
        self.submit_button['font'] = tkfont.Font(family="Helvetica",size=20,weight="bold")
        
        self.input = tk.Entry(self,width=7,font='Helvetica 200')
        with open("./lib/map.json","r") as f:
            map = json.load(f)
        self.input.insert(0, str(len(map)+1))
        self.input.focus_set()
        
        self.back_button.grid(row = 0, column = 0, sticky = "nsew" ,pady = 100,padx=10)
        self.submit_button.grid(row = 0, column = 1,sticky = "nsew" ,pady=100,padx=10)   
        self.input.grid(row=1,column = 0, columnspan=2, padx=10)
    
    def reset_frame(self):
        self.input.delete(0, "end")
        with open("./lib/map.json","r") as f:
            map = json.load(f)
        self.input.insert(0, str(len(map)+1))
        self.input.focus_set()

    def back_cmd(self):
        self.reset_frame()
        self.controller.show_frame("lobby_gui_class")

    def submit_cmd(self):
        input = self.input.get().replace(" ","")
        with open("./lib/map.json","r") as f:
            map = json.load(f)
        if input.isdigit():
            if int(input) ==len(map)+1:
                self.reset_frame()
                with open("./lib/current_sel.json","r") as f:
                    current_sel = json.load(f)
                current_sel["sel"]["mode"]="edit"
                current_sel["sel"]["edit"]["mode"]="new"
                current_sel["sel"]["edit"]["level"]=int(input)
                with open("./lib/current_sel.json","w") as f:
                    f.write(json.dumps(current_sel))
                self.controller.show_frame("edit_new_board_gui_class")
            elif int(input)<len(map)+1 and int(input)>=1:
                self.reset_frame()
                with open("./lib/current_sel.json","r") as f:
                    current_sel = json.load(f)
                current_sel["sel"]["mode"]="edit"
                current_sel["sel"]["edit"]["mode"]="old"
                current_sel["sel"]["edit"]["level"]=int(input)
                current_sel["sel"]["edit"]["height"]=len(map[str(int(input))])
                current_sel["sel"]["edit"]["width"]=len(map[str(int(input))][0])
                with open("./lib/current_sel.json","w") as f:
                    f.write(json.dumps(current_sel))
                self.controller.show_frame("edit_gui_class")
