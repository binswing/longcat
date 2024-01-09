import tkinter as tk       
from tkinter import font as tkfont 
from tkinter import messagebox as msgbox
import threading
from src.play import *
from pynput import keyboard
import time
import json

class speed_run_gui_class(tk.Frame):
    def __init__(self, parent, controller):
        self.CANVA_SIZE = 890
        self.box_arr=[]
        self.select_box_arr=[]
        self.select_box=[0,0]
        self.inframe = False
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.instruction_label = tk.Canvas(self,width=550, height = 110, bg = "#43766C",highlightthickness=0)
        self.instruction_label.create_text(280,50,fill="black", font=("Comfortaa","50","bold"), text="SPEEDRUN")
        self.time_box = tk.Canvas(self,width=320, height = 110, bg = "#43766C",highlightthickness=0)
        self.back_button = tk.Button(self,text='Back',height = 4, width= 10,command= lambda: self.back_cmd(), bg = "#F8FAE5",fg="#76453B",borderwidth=0)
        self.start_play_button = tk.Button(self,text='Start play',height = 4, width= 10,command= lambda: self.start_play_button_cmd(), bg = "#F8FAE5",fg="#76453B",borderwidth=0, disabledforeground="#F2F1EB")
        self.retry_button = tk.Button(self,text='Retry',height = 4, width= 10,command= lambda: self.retry_cmd(), bg = "#F8FAE5",fg="#76453B",borderwidth=0,state="disabled", disabledforeground="#F2F1EB")
        self.reset_button = tk.Button(self,text='Reset',height = 4, width= 10,command= lambda: self.reset_cmd(), bg = "#F8FAE5",fg="#76453B",borderwidth=0,state="disabled", disabledforeground="#F2F1EB")
        self.blank1_button = tk.Button(self,text='',height = 4, width= 10, bg = "#F8FAE5",fg="#76453B",borderwidth=0,state="disabled", disabledforeground="#F2F1EB")
        self.blank2_button = tk.Button(self,text='',height = 4, width= 10, bg = "#F8FAE5",fg="#76453B",borderwidth=0,state="disabled", disabledforeground="#F2F1EB")
        self.blank3_button = tk.Button(self,text='',height = 4, width= 10, bg = "#F8FAE5",fg="#76453B",borderwidth=0,state="disabled", disabledforeground="#F2F1EB")
        self.blank4_button = tk.Button(self,text='',height = 4, width= 10, bg = "#F8FAE5",fg="#76453B",borderwidth=0,state="disabled", disabledforeground="#F2F1EB")
        self.display = tk.Canvas(self,width=890, height = 890, bg = "#f1f1f0",highlightthickness=0)
        
        self.back_button['font'] = tkfont.Font(family="Helvetica",size=15,weight="bold")
        self.start_play_button['font'] = tkfont.Font(family="Helvetica",size=15,weight="bold")
        self.retry_button['font'] = tkfont.Font(family="Helvetica",size=15,weight="bold")
        self.reset_button['font'] = tkfont.Font(family="Helvetica",size=15,weight="bold") 
        self.blank1_button['font'] = tkfont.Font(family="Helvetica",size=15,weight="bold")
        self.blank2_button['font'] = tkfont.Font(family="Helvetica",size=15,weight="bold")
        self.blank3_button['font'] = tkfont.Font(family="Helvetica",size=15,weight="bold")
        self.blank4_button['font'] = tkfont.Font(family="Helvetica",size=15,weight="bold")

        self.back_button.grid(row = 0, column = 0, sticky = "nsew" ,pady = 10,padx=10)
        self.start_play_button.grid(row = 1, column = 0,sticky = "nsew",pady = 10,padx=10)   
        self.retry_button.grid(row = 2, column = 0,sticky = "nsew",pady = 10,padx=10)
        self.reset_button.grid(row = 3, column = 0,sticky = "nsew",pady = 10,padx=10)   
        self.blank1_button.grid(row = 4, column = 0,sticky = "nsew",pady = 10,padx=10)   
        self.blank2_button.grid(row = 5, column = 0,sticky = "nsew" ,pady = 10,padx=10)
        self.blank3_button.grid(row = 6, column = 0, sticky = "nsew" ,pady = 10,padx=10)
        self.blank4_button.grid(row = 7, column = 0, sticky = "nsew" ,pady = 10,padx=10)

        self.instruction_label.grid(row = 0, column = 1,sticky = "nsew" ,pady = 10,padx=10)
        self.time_box.grid(row = 0, column = 2,sticky = "nsew" ,pady = 10,padx=10)
        self.display.grid(row = 1, column = 1,rowspan=7,columnspan=2, sticky = "nsew" ,pady = 10,padx=10)
        self.t2 = threading.Thread(target= self.kb_inp_ctrl)
        self.t2.daemon = True
        self.t2.start() 

    def start_play_button_cmd(self):
        self.inframe = True
        self.box_arr=[]
        self.start_play_button['state'] = "disable"
        self.retry_button['state'] = "normal"
        self.reset_button['state'] = "normal"

        self.logic = logic()
        height,width = self.logic.game.get_board_size()
        box_size = min(int(self.CANVA_SIZE/height),int(self.CANVA_SIZE/width))

        self.x_align=int((self.CANVA_SIZE-width*box_size)/2)
        self.y_align=int((self.CANVA_SIZE-height*box_size)/2)

        self.timelimit = 100*60-1
        self.time = 0
        self.time_display = self.time_box.create_text(165,50,fill="black", font=("Comfortaa","50","bold"), text="00:00")
        self.after(1000, self.time_display_cmd)

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

    def reset_cmd(self):
        self.display.delete("all")
        self.time_box.delete("all")
        self.start_play_button_cmd()

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
    
    def finish_screen(self):
        self.inframe = False
        self.after_cancel(self.timer)
        time.sleep(0.2)
        self.display.delete("all")
        self.display.configure(bg="#F2FFE9")
        self.display.create_text(self.CANVA_SIZE/2,self.CANVA_SIZE/2,fill="black", font=("Helvetica","100","bold"), text="FINISHED!!!")
    
    def lose_screen(self):
        self.inframe = False
        self.retry_button["state"]="disable"
        time.sleep(0.2)
        self.display.delete("all")
        self.display.configure(bg="#F2FFE9")
        self.display.create_text(self.CANVA_SIZE/2,self.CANVA_SIZE/2,fill="black", font=("Helvetica","100","bold"), text="YOU LOSE")    
    
    def retry_cmd(self):
        self.inframe = True
        self.logic.retry()
        self.reset_board()
        self.draw_board(self.logic.game.get_board())

    def time_display_cmd(self):
        self.time+=1
        second = str(self.time % 60)
        minute = str(int((self.time - self.time % 60)/60))
        while len(second) < 2: second = "0" + second
        while len(minute) < 2: minute = "0" + minute
        if self.time < self.timelimit:
            self.time_box.itemconfig(self.time_display,text=minute + ":" + second)
            self.timer = self.after(1000, self.time_display_cmd)
        else:
            self.after_cancel(self.timer)
            self.lose_screen()
        

    def next_cmd(self):
        self.inframe = True
        with open("./src/lib/map.json","r") as f:
            map = json.load(f)
        if self.logic.lvl < len(map.keys()):
            self.logic.next()
            self.reset_board()
            self.draw_board(self.logic.game.get_board())
        else:
            self.finish_screen()

    def reset_frame(self):
        self.display.delete("all")
        self.time_box.delete("all")
        self.start_play_button['state'] = "normal"
        self.retry_button['state'] = "disable"
        self.reset_button['state'] = "disable"

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
                self.next_cmd()

    def down(self):
        if self.inframe:
            self.draw_board(self.logic.game.move("down"))
            if self.logic.game.is_win():
                self.next_cmd()

    def left(self):
        if self.inframe:    
            self.draw_board(self.logic.game.move("left"))
            if self.logic.game.is_win():
                self.next_cmd()

    def right(self):
        if self.inframe:
            self.draw_board(self.logic.game.move("right"))
            if self.logic.game.is_win():
                self.next_cmd()

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
        self.game.import_board(1)
        self.lvl = 1
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