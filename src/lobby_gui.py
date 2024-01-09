import tkinter as tk       
from tkinter import font as tkfont 
import threading
from src.head import *
from pynput import keyboard
import time

class lobby_gui_class(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        self.edit_button = tk.Button(self,text='EDIT',height = 5, width= 20,command= lambda: controller.show_frame("edit_level_selection_gui_class"), bg = "#F8FAE5",fg="#76453B",borderwidth=0)
        self.play_button = tk.Button(self,text='PLAY',height = 5, width= 20,command= lambda: controller.show_frame("play_level_selection_gui_class"), bg = "#F8FAE5",fg="#76453B",borderwidth=0)
        self.speed_run_button = tk.Button(self,text='SPEEDRUN',height = 5, width= 20,command= lambda: controller.show_frame("speed_run_gui_class"), bg = "#F8FAE5",fg="#76453B",borderwidth=0)
        self.edit_button['font'] = tkfont.Font(family="Helvetica",size=35,weight="bold")
        self.play_button['font'] = tkfont.Font(family="Helvetica",size=35,weight="bold")
        self.speed_run_button['font'] = tkfont.Font(family="Helvetica",size=35,weight="bold")
        self.edit_button.grid(row = 0, column = 0, sticky = "nsew" ,pady = 15,padx=230)
        self.play_button.grid(row = 1, column = 0, sticky = "nsew" ,pady = 15,padx=230) 
        self.speed_run_button.grid(row = 2, column = 0, sticky = "nsew" ,pady = 15,padx=230)      