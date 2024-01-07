from src import main_gui
from src.board import *
from pynput import keyboard
import time

class main_class:
    def __init__(self):
        self.app = main_gui.SampleApp()
        self.app.mainloop()

if __name__ == "__main__":
    main_class()    
    