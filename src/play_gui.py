import tkinter as tk       
from tkinter import font as tkfont 
from tkinter import messagebox as msgbox
import threading
from src.play import *
from pynput import keyboard
import time
import json

class play_gui_class(tk.Frame):
    def __init__(self, parent, controller):
        self.CANVA_SIZE = 890
        self.box_arr=[]
        self.select_box_arr=[]
        self.select_box=[0,0]
        self.inframe = False
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.instruction_label = tk.Canvas(self,width=550, height = 110, bg = "#43766C",highlightthickness=0)
        self.instruction_label.create_text(280,50,fill="black", font=("Comfortaa","50","bold"), text="EDIT LEVEL")
        self.lvl_box = tk.Canvas(self,width=320, height = 110, bg = "#43766C",highlightthickness=0)
        self.back_button = tk.Button(self,text='Back',height = 4, width= 10,command= lambda: self.back_cmd(), bg = "#F8FAE5",fg="#76453B",borderwidth=0)
        self.start_play_button = tk.Button(self,text='Start play',height = 4, width= 10,command= lambda: self.start_play_button_cmd(), bg = "#F8FAE5",fg="#76453B",borderwidth=0, disabledforeground="#F2F1EB")
        self.retry_button = tk.Button(self,text='Retry',height = 4, width= 10,command= lambda: self.retry_cmd(), bg = "#F8FAE5",fg="#76453B",borderwidth=0,state="disabled", disabledforeground="#F2F1EB")
        self.previous_button = tk.Button(self,text='Previous',height = 4, width= 10,command= lambda: self.previous_cmd(), bg = "#F8FAE5",fg="#76453B",borderwidth=0,state="disabled", disabledforeground="#F2F1EB")
        self.next_button = tk.Button(self,text='Next',height = 4, width= 10,command= lambda: self.next_cmd(), bg = "#F8FAE5",fg="#76453B",borderwidth=0,state="disabled", disabledforeground="#F2F1EB")
        self.undo_button = tk.Button(self,text='Undo',height = 4, width= 10,command= lambda: self.undo_cmd(), bg = "#F8FAE5",fg="#76453B",borderwidth=0,state="disabled", disabledforeground="#F2F1EB")
        self.first_button = tk.Button(self,text='First',height = 4, width= 10,command= lambda: self.first_cmd(), bg = "#F8FAE5",fg="#76453B",borderwidth=0,state="disabled", disabledforeground="#F2F1EB")
        self.last_button = tk.Button(self,text='Last',height = 4, width= 10,command= lambda: self.last_cmd(), bg = "#F8FAE5",fg="#76453B",borderwidth=0,state="disabled", disabledforeground="#F2F1EB")
        self.display = tk.Canvas(self,width=890, height = 890, bg = "#f1f1f0",highlightthickness=0)
        
        self.back_button['font'] = tkfont.Font(family="Helvetica",size=15,weight="bold")
        self.start_play_button['font'] = tkfont.Font(family="Helvetica",size=15,weight="bold")
        self.retry_button['font'] = tkfont.Font(family="Helvetica",size=15,weight="bold")
        self.previous_button['font'] = tkfont.Font(family="Helvetica",size=15,weight="bold") 
        self.next_button['font'] = tkfont.Font(family="Helvetica",size=15,weight="bold")
        self.undo_button['font'] = tkfont.Font(family="Helvetica",size=15,weight="bold")
        self.first_button['font'] = tkfont.Font(family="Helvetica",size=15,weight="bold")
        self.last_button['font'] = tkfont.Font(family="Helvetica",size=15,weight="bold")

        self.back_button.grid(row = 0, column = 0, sticky = "nsew" ,pady = 10,padx=10)
        self.start_play_button.grid(row = 1, column = 0,sticky = "nsew",pady = 10,padx=10)   
        self.retry_button.grid(row = 2, column = 0,sticky = "nsew",pady = 10,padx=10)
        self.previous_button.grid(row = 3, column = 0,sticky = "nsew",pady = 10,padx=10)   
        self.next_button.grid(row = 4, column = 0,sticky = "nsew",pady = 10,padx=10)   
        self.undo_button.grid(row = 5, column = 0,sticky = "nsew" ,pady = 10,padx=10)
        self.first_button.grid(row = 6, column = 0, sticky = "nsew" ,pady = 10,padx=10)
        self.last_button.grid(row = 7, column = 0, sticky = "nsew" ,pady = 10,padx=10)

        self.instruction_label.grid(row = 0, column = 1,sticky = "nsew" ,pady = 10,padx=10)
        self.lvl_box.grid(row = 0, column = 2,sticky = "nsew" ,pady = 10,padx=10)
        self.display.grid(row = 1, column = 1,rowspan=7,columnspan=2, sticky = "nsew" ,pady = 10,padx=10)
        self.t2 = threading.Thread(target= self.kb_inp_ctrl)
        self.t2.daemon = True
        self.t2.start() 

    def start_play_button_cmd(self):
        self.inframe = True
        self.box_arr=[]
        self.start_play_button['state'] = "disable"
        self.retry_button['state'] = "normal"
        self.previous_button['state'] = "normal"
        self.next_button['state'] = "normal"
        self.undo_button['state'] = "normal"
        self.first_button['state'] = "normal"
        self.last_button['state'] = "normal"

        self.logic = logic()
        height,width = self.logic.game.get_board_size()
        box_size = min(int(self.CANVA_SIZE/height),int(self.CANVA_SIZE/width))

        self.x_align=int((self.CANVA_SIZE-width*box_size)/2)
        self.y_align=int((self.CANVA_SIZE-height*box_size)/2)

        self.lvl_box.create_text(165,50,fill="black", font=("Comfortaa","50","bold"), text=str(self.logic.lvl))

        for i in range(height):
            temp_arr = []
            for j in range(width):
                temp_arr.append(self.display.create_rectangle(j*box_size+self.x_align,i*box_size+self.y_align,(j+1)*box_size+self.x_align,(i+1)*box_size+self.y_align,outline="",fill="#F2FFE9"))
            self.box_arr.append(temp_arr)
        self.draw_board(self.logic.game.get_board())
        
        for i in range(height):
            self.display.create_line(0+self.x_align,i*box_size+self.y_align,width*box_size+self.x_align,i*box_size+self.y_align,fill="black")
        self.display.create_line(0+self.x_align,height*box_size-1+self.y_align,width*box_size+self.x_align,height*box_size-1+self.y_align,fill="black")
        for i in range(width):
            self.display.create_line(i*box_size+self.x_align,0+self.y_align,i*box_size+self.x_align,height*box_size+self.y_align,fill="black")
        self.display.create_line(width*box_size-1+self.x_align,0+self.y_align,width*box_size-1+self.x_align,height*box_size+self.y_align,fill="black")

    def reset_board(self):
        self.display.delete("all")
        self.box_arr=[]

        self.display.configure(bg="#f1f1f0")

        height,width = self.logic.game.get_board_size()
        box_size = min(int(self.CANVA_SIZE/height),int(self.CANVA_SIZE/width))

        self.x_align=int((self.CANVA_SIZE-width*box_size)/2)
        self.y_align=int((self.CANVA_SIZE-height*box_size)/2)

        for i in range(height):
            temp_arr = []
            for j in range(width):
                temp_arr.append(self.display.create_rectangle(j*box_size+self.x_align,i*box_size+self.y_align,(j+1)*box_size+self.x_align,(i+1)*box_size+self.y_align,outline="",fill="#F2FFE9"))
            self.box_arr.append(temp_arr)

        self.draw_board(self.logic.game.get_board())
        
        for i in range(height):
            self.display.create_line(0+self.x_align,i*box_size+self.y_align,width*box_size+self.x_align,i*box_size+self.y_align,fill="black")
        self.display.create_line(0+self.x_align,height*box_size-1+self.y_align,width*box_size+self.x_align,height*box_size-1+self.y_align,fill="black")
        for i in range(width):
            self.display.create_line(i*box_size+self.x_align,0+self.y_align,i*box_size+self.x_align,height*box_size+self.y_align,fill="black")
        self.display.create_line(width*box_size-1+self.x_align,0+self.y_align,width*box_size-1+self.x_align,height*box_size+self.y_align,fill="black")
    
    def win_screen(self):
        self.inframe = False
        time.sleep(0.2)
        self.display.delete("all")
        self.display.configure(bg="#F2FFE9")
        self.display.create_text(445,445,fill="black", font=("Helvetica","100","bold"), text="YOU WIN")
    
    def lose_screen(self):
        self.inframe = False
        time.sleep(0.2)
        self.display.delete("all")
        self.display.configure(bg="#F2FFE9")
        self.display.create_text(445,445,fill="black", font=("Helvetica","100","bold"), text="YOU LOSE")    
    
    def previous_cmd(self): 
        self.inframe = True
        if self.logic.lvl > 1:
            self.logic.previous()
            self.lvl_box.delete("all")
            self.lvl_box.create_text(165,50,fill="black", font=("Comfortaa","50","bold"), text=str(self.logic.lvl))
            self.reset_board()
            self.draw_board(self.logic.game.get_board())

    def first_cmd(self): 
        self.inframe = True
        self.logic.first()
        self.lvl_box.delete("all")
        self.lvl_box.create_text(165,50,fill="black", font=("Comfortaa","50","bold"), text=str(self.logic.lvl))
        self.reset_board()
        self.draw_board(self.logic.game.get_board())

    def last_cmd(self): 
        self.inframe = True
        self.logic.last()
        self.lvl_box.delete("all")
        self.lvl_box.create_text(165,50,fill="black", font=("Comfortaa","50","bold"), text=str(self.logic.lvl))
        self.reset_board()
        self.draw_board(self.logic.game.get_board())

    def retry_cmd(self):
        self.inframe = True
        self.logic.retry()
        self.lvl_box.delete("all")
        self.lvl_box.create_text(165,50,fill="black", font=("Comfortaa","50","bold"), text=str(self.logic.lvl))
        self.reset_board()
        self.draw_board(self.logic.game.get_board())

    def next_cmd(self):
        self.inframe = True
        with open("./src/lib/map.json","r") as f:
            map = json.load(f)
        if self.logic.lvl < len(map.keys()):
            self.logic.next()
            self.lvl_box.delete("all")
            self.lvl_box.create_text(165,50,fill="black", font=("Comfortaa","50","bold"), text=str(self.logic.lvl))
            self.reset_board()
            self.draw_board(self.logic.game.get_board())
        
    def undo_cmd(self):
        self.draw_board(self.logic.game.undo_step())

    def reset_frame(self):
        self.display.delete("all")
        self.lvl_box.delete("all")
        self.start_play_button['state'] = "normal"
        self.retry_button['state'] = "disable"
        self.previous_button['state'] = "disable"
        self.next_button['state'] ="disable"
        self.undo_button['state'] ="disable"
        self.first_button['state'] = "disable"
        self.last_button['state'] = "disable"

    def back_cmd(self):
        self.inframe = False
        self.reset_frame()
        self.controller.show_frame("lobby_gui_class")

    def draw_board(self,board):
        if len(board) != 0:
            if type(board[0][0]) is not list:
                self.draw_board_func(board)
            else:
                for k in board:
                    self.draw_board_func(k)
        
    def draw_board_func(self,board):
        for y in range(self.logic.height):
            for x in range(self.logic.width):
                if board[y][x] == 0:
                    self.display.itemconfig(self.box_arr[y][x],fill="#F2FFE9")
                elif board[y][x] == 1:
                    self.display.itemconfig(self.box_arr[y][x],fill="#FA7070")
                elif board[y][x] == 2:
                    self.display.itemconfig(self.box_arr[y][x],fill="#557C55")
                elif board[y][x] == 3:
                    self.display.itemconfig(self.box_arr[y][x],fill="#A6CF98")   

    def up(self):
        if self.inframe:
            self.draw_board(self.logic.game.move("up"))
            if self.logic.game.is_win():
                self.win_screen()
            elif self.logic.game.is_lose():
                self.lose_screen()    

    def down(self):
        if self.inframe:
            self.draw_board(self.logic.game.move("down"))
            if self.logic.game.is_win():
                self.win_screen()
            elif self.logic.game.is_lose():
                self.lose_screen()  

    def left(self):
        if self.inframe:    
            self.draw_board(self.logic.game.move("left"))
            if self.logic.game.is_win():
                self.win_screen()
            elif self.logic.game.is_lose():
                self.lose_screen()  

    def right(self):
        if self.inframe:
            self.draw_board(self.logic.game.move("right"))
            if self.logic.game.is_win():
                self.win_screen()
            elif self.logic.game.is_lose():
                self.lose_screen()  

    def on_release(self,key):
        if key == keyboard.Key.up or key == keyboard.KeyCode.from_char("w"): self.up()
        elif key == keyboard.Key.down or key == keyboard.KeyCode.from_char("s"): self.down()
        elif key == keyboard.Key.left or key == keyboard.KeyCode.from_char("a"): self.left()
        elif key == keyboard.Key.right or key == keyboard.KeyCode.from_char("d"): self.right()

    def kb_inp_ctrl(self):
        with keyboard.Listener(on_release= self.on_release) as listener:
            listener.join()

class logic:
    def __init__(self,CANVA_SIZE=890):
        self.CANVA_SIZE = CANVA_SIZE
        self.game = Play()
        with open("./src/lib/current_sel.json","r") as f:
            current_sel = json.load(f)
        self.game.import_board(current_sel["sel"]["play"]["level"])
        self.lvl = current_sel["sel"]["play"]["level"]
        self.height,self.width = self.game.get_board_size()
        self.box_size = min(int(self.CANVA_SIZE/self.height),int(self.CANVA_SIZE/self.width))
    
    def retry(self):
        self.game = Play()
        self.game.import_board(self.lvl)
    
    def next(self):
        self.lvl +=1
        self.retry()
        self.height,self.width = self.game.get_board_size()
        self.box_size = min(int(self.CANVA_SIZE/self.height),int(self.CANVA_SIZE/self.width))
    
    def previous(self):
        self.lvl -=1
        self.retry()
        self.height,self.width = self.game.get_board_size()
        self.box_size = min(int(self.CANVA_SIZE/self.height),int(self.CANVA_SIZE/self.width))
    
    def first(self):
        self.lvl = 1
        self.retry()
        self.height,self.width = self.game.get_board_size()
        self.box_size = min(int(self.CANVA_SIZE/self.height),int(self.CANVA_SIZE/self.width))
    
    def last(self):
        with open("./src/lib/map.json","r") as f:
            map = json.load(f)        
        self.lvl = len(map.keys())
        self.retry()
        self.height,self.width = self.game.get_board_size()
        self.box_size = min(int(self.CANVA_SIZE/self.height),int(self.CANVA_SIZE/self.width))