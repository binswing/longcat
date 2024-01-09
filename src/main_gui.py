import tkinter as tk       
from tkinter import font as tkfont 
import threading
from src.head import *
from pynput import keyboard
import time 
        
class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        container = tk.Frame(self,bg= "#43766C",width=1000,height=1000)
        container.pack(side="top", fill="both", expand=False)


        self.frames = {}
        for F in (lobby_gui_class, edit_level_selection_gui_class, play_level_selection_gui_class, edit_new_board_gui_class,edit_gui_class,play_gui_class,speed_run_gui_class):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame 
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("lobby_gui_class")

    def show_frame(self, page_name,):
        frame = self.frames[page_name]
        frame.tkraise()

