import tkinter as tk       
from tkinter import font as tkfont 
import threading
from pynput import keyboard
import time
import json

class edit_new_board_gui_class(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        self.back_button = tk.Button(self,text='BACK',height = 8, width= 17,command= lambda: controller.show_frame("edit_level_selection_gui_class"), bg = "#F8FAE5",fg="#76453B",borderwidth=0)
        self.submit_button = tk.Button(self,text='SUBMIT LEVEL',height = 8, width= 30,command= lambda: self.submit_cmd(), bg = "#F8FAE5",fg="#76453B",borderwidth=0)
        self.back_button['font'] = tkfont.Font(family="Helvetica",size=20,weight="bold")
        self.submit_button['font'] = tkfont.Font(family="Helvetica",size=20,weight="bold")
        
        self.height_label = tk.Label(self, text = "Height",font=("Comfortaa", 30,"bold"))
        self.width_label = tk.Label(self, text = "Width",font=("Comfortaa",  30,"bold"))
        self.height_input = tk.Entry(self,width=5,font='Helvetica 50')
        self.width_input = tk.Entry(self,width=5,font='Helvetica 50')
        self.height_input.focus_set()

        self.back_button.grid(row = 0, column = 0, sticky = "nsew" ,pady = 100,padx=60)
        self.submit_button.grid(row = 0, column = 1,sticky = "nsew" ,pady=100,padx=60) 
        self.height_label.grid(row=1,column = 0, sticky = "nsew",pady = 90, padx=60)
        self.width_label.grid(row=2,column = 0, sticky = "nsew",pady = 90, padx=60)  
        self.height_input.grid(row=1,column = 1, sticky = "nsew",pady = 90, padx=60)
        self.width_input.grid(row=2,column = 1, sticky = "nsew",pady = 90, padx=60)

    def reset_frame(self):
        self.height_input.delete(0, "end")
        self.width_input.delete(0, "end")
        self.height_input.focus_set()

    def submit_cmd(self):
        height_input = self.height_input.get().replace(" ","")
        width_input = self.width_input.get().replace(" ","")
        if height_input.isdigit() and width_input.isdigit():
            if int(height_input)<=10 and int(width_input)<=10 and int(height_input)>=2 and int(width_input)>=2:
                self.reset_frame()
                with open("./src/lib/current_sel.json","r") as f:
                    current_sel = json.load(f)
                current_sel["sel"]["edit"]["height"]=int(height_input)
                current_sel["sel"]["edit"]["width"]=int(width_input)
                with open("./src/lib/current_sel.json","w") as f:
                    f.write(json.dumps(current_sel))                
                self.controller.show_frame("edit_gui_class")  