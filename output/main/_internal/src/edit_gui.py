import tkinter as tk       
from tkinter import font as tkfont 
from tkinter import messagebox as msgbox
import threading
from src.edit import *
from src.play import *
from pynput import keyboard
import time
import json

class edit_gui_class(tk.Frame):
    def __init__(self, parent, controller):
        self.CANVA_SIZE = 890
        self.box_arr=[]
        self.select_box_arr=[]
        self.select_box=[0,0]
        self.inframe = False
        self.mode= True #True-edit False-play
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.instruction_label = tk.Canvas(self,width=550, height = 110, bg = "#43766C",highlightthickness=0)
        self.instruction_label.create_text(280,50,fill="black", font=("Comfortaa","50","bold"), text="EDIT LEVEL")
        self.lvl_box = tk.Canvas(self,width=320, height = 110, bg = "#43766C",highlightthickness=0)
        self.back_button = tk.Button(self,text='Back',height = 4, width= 10,command= lambda: self.back_cmd(), bg = "#F8FAE5",fg="#76453B",borderwidth=0)
        self.start_edit_button = tk.Button(self,text='Start edit',height = 4, width= 10,command= lambda: self.start_edit_button_cmd(), bg = "#F8FAE5",fg="#76453B",borderwidth=0, disabledforeground="#F2F1EB")
        self.save_button = tk.Button(self,text='Save',height = 4, width= 10,command= lambda: self.save_cmd(), bg = "#F8FAE5",fg="#76453B",borderwidth=0,state="disabled", disabledforeground="#F2F1EB")
        self.clear_board_button = tk.Button(self,text='Clear board',height = 4, width= 10,command= lambda: self.clear_board_cmd(), bg = "#F8FAE5",fg="#76453B",borderwidth=0,state="disabled", disabledforeground="#F2F1EB")
        self.wall_button = tk.Button(self,text='Wall',height = 4, width= 10,command= lambda: self.wall_cmd(), bg = "#F8FAE5",fg="#76453B",borderwidth=0,state="disabled", disabledforeground="#F2F1EB")
        self.head_button = tk.Button(self,text='Head',height = 4, width= 10,command= lambda: self.head_cmd(), bg = "#F8FAE5",fg="#76453B",borderwidth=0,state="disabled", disabledforeground="#F2F1EB")
        self.clear_wall_button = tk.Button(self,text='Clear wall',height = 4, width= 10,command= lambda: self.clear_wall_cmd(), bg = "#F8FAE5",fg="#76453B",borderwidth=0,state="disabled", disabledforeground="#F2F1EB")
        self.clear_head_button = tk.Button(self,text='Auto\nset head',height = 4, width= 10,command= lambda: self.auto_set_head(), bg = "#F8FAE5",fg="#76453B",borderwidth=0,state="disabled", disabledforeground="#F2F1EB")
        self.display = tk.Canvas(self,width=890, height = 890, bg = "#f1f1f0",highlightthickness=0)
        
        self.back_button['font'] = tkfont.Font(family="Helvetica",size=15,weight="bold")
        self.start_edit_button['font'] = tkfont.Font(family="Helvetica",size=15,weight="bold")
        self.save_button['font'] = tkfont.Font(family="Helvetica",size=15,weight="bold")
        self.clear_board_button['font'] = tkfont.Font(family="Helvetica",size=15,weight="bold") 
        self.wall_button['font'] = tkfont.Font(family="Helvetica",size=15,weight="bold")
        self.head_button['font'] = tkfont.Font(family="Helvetica",size=15,weight="bold")
        self.clear_wall_button['font'] = tkfont.Font(family="Helvetica",size=15,weight="bold")
        self.clear_head_button['font'] = tkfont.Font(family="Helvetica",size=15,weight="bold")

        self.back_button.grid(row = 0, column = 0, sticky = "nsew" ,pady = 10,padx=10)
        self.start_edit_button.grid(row = 1, column = 0,sticky = "nsew",pady = 10,padx=10)   
        self.save_button.grid(row = 2, column = 0,sticky = "nsew",pady = 10,padx=10)
        self.clear_board_button.grid(row = 3, column = 0,sticky = "nsew",pady = 10,padx=10)   
        self.wall_button.grid(row = 4, column = 0,sticky = "nsew",pady = 10,padx=10)   
        self.head_button.grid(row = 5, column = 0,sticky = "nsew" ,pady = 10,padx=10)
        self.clear_wall_button.grid(row = 6, column = 0, sticky = "nsew" ,pady = 10,padx=10)
        self.clear_head_button.grid(row = 7, column = 0, sticky = "nsew" ,pady = 10,padx=10)

        self.instruction_label.grid(row = 0, column = 1,sticky = "nsew" ,pady = 10,padx=10)
        self.lvl_box.grid(row = 0, column = 2,sticky = "nsew" ,pady = 10,padx=10)
        self.display.grid(row = 1, column = 1,rowspan=7,columnspan=2, sticky = "nsew" ,pady = 10,padx=10)
        self.t1 = threading.Thread(target= self.kb_inp_ctrl)
        self.t1.daemon = True
        self.t1.start() 

    def start_edit_button_cmd(self):
        self.inframe = True
        self.mode= True
        self.box_arr=[]
        self.select_box_arr=[]
        self.select_box=[0,0]
        self.start_edit_button.configure(text="Edit mode",command= lambda: self.play_mode_cmd())
        self.save_button['state'] = "normal"
        self.clear_board_button['state'] = "normal"
        self.wall_button['text'] ="Wall selected"
        self.head_button['state'] = "normal"
        self.clear_wall_button['state'] ="normal"
        self.clear_head_button['state'] ="normal"

        self.logic = logic()
        height,width = self.logic.game.get_board_size()
        box_size = min(int(self.CANVA_SIZE/height),int(self.CANVA_SIZE/width))
        
        if self.logic.game.is_head_set():
            self.clear_head_button.configure(text="Clear head",command=lambda:self.clear_head_cmd())

        self.x_align=int((self.CANVA_SIZE-width*box_size)/2)
        self.y_align=int((self.CANVA_SIZE-height*box_size)/2)

        self.lvl_box.create_text(165,50,fill="black", font=("Comfortaa","50","bold"), text=str(self.logic.game.get_lvl()))

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

        for i in range(height-1):
            temp_arr = []
            for j in range(width-1):
                temp_arr.append(self.display.create_rectangle(j*box_size+self.x_align,i*box_size+self.y_align,(j+1)*box_size+self.x_align,(i+1)*box_size+self.y_align,width=2,outline="",fill=""))
            temp_arr.append(self.display.create_rectangle((width-1)*box_size+self.x_align,i*box_size+self.y_align,width*box_size-1+self.x_align,(i+1)*box_size+self.y_align,width=2,outline="",fill=""))
            self.select_box_arr.append(temp_arr)
        temp_arr = []
        for j in range(width-1):
            temp_arr.append(self.display.create_rectangle(j*box_size+self.x_align,(height-1)*box_size+self.y_align,(j+1)*box_size+self.x_align,height*box_size-1+self.y_align,width=2,outline="",fill=""))
        temp_arr.append(self.display.create_rectangle((width-1)*box_size+self.x_align,(height-1)*box_size+self.y_align,width*box_size-1+self.x_align,height*box_size-1+self.y_align,width=2,outline="",fill=""))
        self.select_box_arr.append(temp_arr)

        self.display.itemconfig(self.select_box_arr[self.select_box[1]][self.select_box[0]],outline="blue")

    def play_mode_cmd(self):
        self.mode= False
        self.logic.game_mode()
        self.start_edit_button.configure(text="Play mode",command= lambda: self.edit_mode_cmd())
        self.save_button.configure(text="Retry",command= lambda: self.retry_cmd())
        self.display.itemconfig(self.select_box_arr[self.select_box[1]][self.select_box[0]],outline="")
        self.clear_board_button['state'] = "disable"
        self.clear_wall_button['state'] ="disable"
        self.clear_head_button['state'] ="disable"
        if self.logic.select_type == "wall":
            self.head_button['state'] = "disable"
            self.wall_button['text'] ="Wall"
        elif self.logic.select_type == "head":
            self.head_button['text'] ="Head"
            self.wall_button['state'] = "disable" 
    
    def retry_cmd(self):
        self.logic.game_mode()
        with open("./lib/current_sel.json","r") as f:
            current_sel = json.load(f)
        self.draw_board(current_sel["map"])

    def edit_mode_cmd(self):
        self.mode= True
        self.draw_board(self.logic.game.get_board())
        self.start_edit_button.configure(text="Edit mode",command= lambda: self.play_mode_cmd())
        self.save_button.configure(text='Save',command= lambda: self.save_cmd())
        self.display.itemconfig(self.select_box_arr[self.select_box[1]][self.select_box[0]],outline="blue")
        self.clear_board_button['state'] = "normal"
        self.clear_wall_button['state'] ="normal"
        self.clear_head_button['state'] ="normal"
        if self.logic.select_type == "wall":
            self.head_button['state'] = "normal"
            self.wall_button['text'] ="Wall selected"
        elif self.logic.select_type == "head":
            self.head_button['text'] ="Head selected"
            self.wall_button['state'] = "normal" 

    def wall_cmd(self):
        self.logic.select_type = "wall"
        self.head_button['state'] ="normal"
        self.wall_button['state'] ="disable"
        self.head_button['text'] = "Head"
        self.wall_button['text'] = "Wall selected" 
    
    def head_cmd(self):
        self.logic.select_type = "head"
        self.wall_button['state'] ="normal"
        self.head_button['state'] ="disable"
        self.wall_button['text'] = "Wall"
        self.head_button['text'] = "Head selected"    

    def change_select_box(self,x,y):
        self.display.itemconfig(self.select_box_arr[y][x],outline="blue")
        self.display.itemconfig(self.select_box_arr[self.select_box[1]][self.select_box[0]],outline="")
        self.select_box=[x,y]

    def reset_frame(self):
        self.display.delete("all")
        self.lvl_box.delete("all")
        self.start_edit_button.configure(text="Start edit",command= lambda:self.start_edit_button_cmd())
        self.save_button.configure(text='Save',command= lambda: self.save_cmd())
        self.save_button['state'] = "disable"
        self.clear_board_button['state'] = "disable"
        self.wall_button['text'] ="Wall"
        self.head_button['text'] = "Head"
        self.wall_button['state'] ="disable"
        self.head_button['state'] = "disable"
        self.clear_wall_button['state'] ="disable"
        self.clear_head_button['state'] ="disable"    

    def back_cmd(self):
        self.inframe = False
        self.reset_frame()
        self.controller.show_frame("lobby_gui_class")

    def save_cmd(self):
        self.inframe = False
        self.logic.game.save_board()
        self.reset_frame()
        self.controller.show_frame("lobby_gui_class")    

    def clear_board_cmd(self): 
        self.draw_board(self.logic.game.clear_board())

    def clear_head_cmd(self): 
        self.draw_board(self.logic.game.clear_head())
        self.clear_head_button.configure(text="Auto\nset head",command=lambda:self.auto_set_head())

    def auto_set_head(self):
        msgbox.showinfo(message="Please wait about 60s until a messagebox pops up after clicking ok!")
        self.draw_board(self.logic.game.auto_set_head())
        if self.logic.game.is_head_set():
            self.clear_head_button.configure(text="Clear head",command=lambda:self.clear_head_cmd())
        else:
            msgbox.showinfo(message="No available head")

    def clear_wall_cmd(self): self.draw_board(self.logic.game.clear_walls())

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
            if self.mode:
                if self.select_box[1]-1 >=0:
                    self.change_select_box(self.select_box[0],self.select_box[1]-1)
                    self.logic.game.move_sel("up")
            else:
                self.draw_board(self.logic.game_clone.move("up"))

    def down(self):
        if self.inframe:
            if self.mode:
                if self.select_box[1]+1 <= self.logic.height-1:
                    self.change_select_box(self.select_box[0],self.select_box[1]+1)
                    self.logic.game.move_sel("down")
            else:
                self.draw_board(self.logic.game_clone.move("down"))

    def left(self):
        if self.inframe:    
            if self.mode:    
                if self.select_box[0]-1 >= 0:
                    self.change_select_box(self.select_box[0]-1,self.select_box[1])
                    self.logic.game.move_sel("left")
            else:
                self.draw_board(self.logic.game_clone.move("left")) 

    def right(self):
        if self.inframe:
            if self.mode:
                if self.select_box[0]+1 <= self.logic.width-1:
                    self.change_select_box(self.select_box[0]+1,self.select_box[1])
                    self.logic.game.move_sel("right")
            else:
                self.draw_board(self.logic.game_clone.move("right")) 

    def enter(self):
        if self.mode: 
            self.draw_board(self.logic.enter_cmd())
            if self.logic.game.is_head_set():
                self.clear_head_button.configure(text="Clear head",command=lambda:self.clear_head_cmd())
            else:
                self.clear_head_button.configure(text="Auto\nset head",command=lambda:self.auto_set_head())

    def on_release(self,key):
        if key == keyboard.Key.up or key == keyboard.KeyCode.from_char("w"): self.up()
        elif key == keyboard.Key.down or key == keyboard.KeyCode.from_char("s"): self.down()
        elif key == keyboard.Key.left or key == keyboard.KeyCode.from_char("a"): self.left()
        elif key == keyboard.Key.right or key == keyboard.KeyCode.from_char("d"): self.right()
        elif key == keyboard.Key.enter or key == keyboard.Key.space: self.enter()

    def kb_inp_ctrl(self):
        with keyboard.Listener(on_release= self.on_release) as listener:
            listener.join()

class logic:
    def __init__(self,CANVA_SIZE=890):
        self.CANVA_SIZE = CANVA_SIZE
        self.game = Edit()
        with open("./lib/current_sel.json","r") as f:
            current_sel = json.load(f)
        if current_sel["sel"]["edit"]["mode"]=="new":
            self.game.new_board(current_sel["sel"]["edit"]["height"],current_sel["sel"]["edit"]["width"])
        elif current_sel["sel"]["edit"]["mode"]=="old":
            self.game.load_board(current_sel["sel"]["edit"]["level"])
        self.height,self.width = self.game.get_board_size()
        self.select_type = "wall"
        self.box_size = min(int(self.CANVA_SIZE/self.height),int(self.CANVA_SIZE/self.width))
    
    def enter_cmd(self):
        if self.select_type == "wall":
            return self.game.set_and_del_wall()
        elif self.select_type == "head":
            return self.game.set_and_del_head()
    
    def game_mode(self):
        with open("./lib/current_sel.json","r") as f:
            current_sel = json.load(f)
        current_sel["map"] = self.game.get_board()
        with open("./lib/current_sel.json","w") as f:
            f.write(json.dumps(current_sel))
        with open("./lib/current_sel.json","r") as f:
            current_sel = json.load(f)
        self.game_clone = Play()
        self.game_clone.load_board(current_sel["map"])