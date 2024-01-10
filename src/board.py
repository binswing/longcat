import json
import time
import copy 
class Board:
    def __init__(self):
        self.board = []
        self.height = 0
        self.width = 0
        self.factor = [0,1,2,3] # 0-blank, 1-wall, 2-head, 3-body
        self.board_list = []

    # board
    def load_board(self,board):
        self.board = board
        self.height = len(self.board)
        self.width = len(self.board[0])
        self.add_board_list()

    def add_board_list(self):
        self.board_list.append(copy.deepcopy(self.board))

    def set_board_size(self,height,width):
        self.width = width
        self.height = height

    def new_board(self,height,width):
        self.board = []
        self.width = width
        self.height = height
        for i in range(height):
            temp_arr = []
            for j in range(width):
                temp_arr.append(0)
            self.board.append(temp_arr)

    def clear_board(self):
        self.new_board(self.height,self.width)
        return self.get_board()
            
    #wall
    def clear_walls(self):
        wall_arr = self.get_wall_coordinate()
        for wall in wall_arr:
            y_wall,x_wall = wall
            self.board[y_wall][x_wall] = 0
        return self.get_board()
                    
    def set_and_del_wall(self,x_wall,y_wall):
        if self.board[y_wall][x_wall] == 1:
            self.board[y_wall][x_wall] = 0
        else:
            self.board[y_wall][x_wall] = 1
        return self.get_board()
            
    #head     
    def clear_head(self):
        if self.is_head_set():
            y_head,x_head = self.get_head_coordinate()
            self.board[y_head][x_head] = 0  
            return self.get_board()

    def set_and_del_head(self,x_head,y_head):
        if self.board[y_head][x_head] == 2:
            self.board[y_head][x_head] = 0
        else:
            if self.is_head_set():
                old_y_head,old_x_head = self.get_head_coordinate()
                self.board[old_y_head][old_x_head] = 0
            self.board[y_head][x_head] = 2  
        return self.get_board()
                
    #move
    def move(self,direction):
        board_process = []
        if self.is_head_set():
            y_head,x_head = self.get_head_coordinate()
            num_of_move = 0
            if direction == "up":
                while y_head-(num_of_move+1) >= 0:
                    if self.board[y_head-(num_of_move+1)][x_head]==0:
                        self.board[y_head-(num_of_move+1)][x_head] = 2
                        self.board[y_head-num_of_move][x_head] = 3
                        board_process.append(self.board.copy())
                        num_of_move+=1
                    else: break
            elif direction == "down":
                while y_head+(num_of_move+1) <= self.height-1:
                    if self.board[y_head+(num_of_move+1)][x_head]==0:
                        self.board[y_head+(num_of_move+1)][x_head] = 2
                        self.board[y_head+num_of_move][x_head] = 3
                        board_process.append(self.board.copy())
                        num_of_move+=1
                    else: break
            elif direction == "left":
                while x_head-(num_of_move+1) >= 0:
                    if self.board[y_head][x_head-(num_of_move+1)]==0:
                        self.board[y_head][x_head-(num_of_move+1)] = 2
                        self.board[y_head][x_head-num_of_move] = 3
                        board_process.append(self.board.copy())
                        num_of_move+=1
                    else: break
            elif direction == "right":
                while x_head+(num_of_move+1) <= self.width-1:
                    if self.board[y_head][x_head+(num_of_move+1)]==0:
                        self.board[y_head][x_head+(num_of_move+1)] = 2
                        self.board[y_head][x_head+num_of_move] = 3
                        board_process.append(self.board.copy())
                        num_of_move+=1
                    else: break
        if len(board_process) != 0:
            self.add_board_list()
        return board_process
    
    def undo_step(self):
        if len(self.board_list) >1:
            self.board_list.pop(-1)         
            self.board = copy.deepcopy(self.board)[-1]
        return self.board

    #auto set head
    def auto_set_head(self):
        pos_arr=[]
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] == 0:
                    step_arr=[[x,y]]
                    status_arr = [copy.deepcopy(self.board)]
                    status_arr[0][y][x]=2
                    step = 1
                    while True:
                        temp_arr=[]
                        for board in status_arr:
                            if type(board) is list:
                                changed_box = self.move_auto_set_head(copy.deepcopy(board),"up")
                                if changed_box != copy.deepcopy(board):
                                    temp_arr.append(copy.deepcopy(changed_box))
                                else:
                                    temp_arr.append(0)
                                changed_box = self.move_auto_set_head(copy.deepcopy(board),"down")
                                if changed_box != copy.deepcopy(board):
                                    temp_arr.append(copy.deepcopy(changed_box))
                                else:
                                    temp_arr.append(0)
                                changed_box = self.move_auto_set_head(copy.deepcopy(board),"right")
                                if changed_box != copy.deepcopy(board):
                                    temp_arr.append(copy.deepcopy(changed_box))
                                else:
                                    temp_arr.append(0)
                                changed_box = self.move_auto_set_head(copy.deepcopy(board),"left")
                                if changed_box != copy.deepcopy(board):
                                    temp_arr.append(copy.deepcopy(changed_box))
                                else:
                                    temp_arr.append(0)
                        if self.check_lose_auto_set_head(temp_arr): 
                            break
                        elif 1 in temp_arr:
                            step_arr.append(step)
                            pos_arr.append(step_arr)
                            break
                        step+=1
                        status_arr = copy.deepcopy(temp_arr)    
                        print(status_arr)                     
          
        if len(pos_arr) !=0:
            pos_dict={}
            for k in pos_arr:
                if str(k[1]) not in pos_dict.keys():
                    pos_dict[str(k[1])] = []
                pos_dict[str(k[1])].append(k[0])
            print(pos_arr)
            pos = pos_dict[str(max([int(i) for i in pos_dict.keys()]))]
            print(pos)
            x = pos[0][0]
            y = pos[0][1]
            print(x,y)
            self.board[y][x]=2

    def move_auto_set_head(self,board,direction):
        for i in range(self.height):
            for j in range(self.width):
                if board[i][j] == 2:
                    y_head = i
                    x_head = j
        num_of_move = 0
        if direction == "up":
            while y_head-(num_of_move+1) >= 0:
                if board[y_head-(num_of_move+1)][x_head]==0:
                    board[y_head-(num_of_move+1)][x_head] = 2
                    board[y_head-num_of_move][x_head] = 3
                    num_of_move+=1
                else: break
        elif direction == "down":
            while y_head+(num_of_move+1) <= self.height-1:
                if board[y_head+(num_of_move+1)][x_head]==0:
                    board[y_head+(num_of_move+1)][x_head] = 2
                    board[y_head+num_of_move][x_head] = 3
                    num_of_move+=1
                else: break
        elif direction == "left":
            while x_head-(num_of_move+1) >= 0:
                if board[y_head][x_head-(num_of_move+1)]==0:
                    board[y_head][x_head-(num_of_move+1)] = 2
                    board[y_head][x_head-num_of_move] = 3
                    num_of_move+=1
                else: break
        elif direction == "right":
            while x_head+(num_of_move+1) <= self.width-1:
                if board[y_head][x_head+(num_of_move+1)]==0:
                    board[y_head][x_head+(num_of_move+1)] = 2
                    board[y_head][x_head+num_of_move] = 3
                    num_of_move+=1
                else: break
        if self.is_win_auto_set_head(board): 
            return 1
        else:
            return board
        
    def is_win_auto_set_head(self,board): 
        state = True
        for i in range(self.height):
            for j in range(self.width):
                if board[i][j] == 0:
                    state = False
                    break
        return state
    
    def check_lose_auto_set_head(self,board): 
        state = True
        for i in board:
            if i != 0:
                state = False
        return state
        
    #info
    def is_win(self): 
        state = True
        for i in range(self.height):
            for j in range(self.width):
                if self.board[i][j] == 0:
                    state = False
                    break
        return state
    
    def is_lose(self): 
        state = True
        y_head, x_head = self.get_head_coordinate()
        if y_head - 1 >= 0: 
            if self.board[y_head-1][x_head] == 0: state = False
        if y_head + 1 <= self.height-1: 
            if self.board[y_head+1][x_head] == 0: state = False
        if x_head - 1 >= 0: 
            if self.board[y_head][x_head-1] == 0: state = False
        if x_head + 1 <= self.width-1: 
            if self.board[y_head][x_head+1] == 0: state = False
        return state

    def is_head_set(self): 
        state = False
        for i in range(self.height):
            for j in range(self.width):
                if self.board[i][j] == 2:
                    state = True
                    break
        return state

    def get_factor(self,x_square,y_square): return self.board[y_square,x_square]
                
    def get_board(self): return self.board.copy()

    def get_board_size(self): return self.height,self.width

    def get_wall_coordinate(self):
        wall_arr = []
        for i in range(self.height):
            for j in range(self.width):
                if self.board[i][j] == 1:
                    wall_arr.append((i,j))
        return wall_arr

    def get_head_coordinate(self):
        for i in range(self.height):
            for j in range(self.width):
                if self.board[i][j] == 2:
                    return i,j  
