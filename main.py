from src import main_gui
from src.board import *
from pynput import keyboard
import time

class main_class:
    def __init__(self):
        self.app = main_gui.SampleApp()
        # self.app.attributes('-fullscreen',True) 
        # self.app.update()
        # print(self.app.winfo_width(),self.app.winfo_height())
        self.app.mainloop()  

if __name__ == "__main__":
    main_class()    
    