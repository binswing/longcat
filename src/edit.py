import json
from src.board import *
class Edit:
    def __init__(self):
        self.board = Board()
        self.selected_square = [0,0]
        self.lvl = 0

    # board
    def new_board(self,height,width):
        self.board.new_board(height,width)
        with open("./src/lib/map.json","r") as f:
            map = json.load(f)
        self.lvl = len(map)+1

    def load_board(self,lvl):
        with open("./src/lib/map.json","r") as f:
            map = json.load(f)
        self.lvl = lvl
        self.board.load_board(map[str(lvl)])

    def save_board(self):
        with open("./src/lib/map.json","r") as f:
            map = json.load(f)
        map[str(self.lvl)] = self.board.get_board().copy()
        with open("./src/lib/map.json","w") as f:
            f.write(json.dumps(map))

    def clear_board(self): return self.board.clear_board()

    #wall
    def clear_walls(self): return self.board.clear_walls()
                    
    def set_and_del_wall(self): return self.board.set_and_del_wall(self.selected_square[0],self.selected_square[1])
            
    #head  
    def clear_head(self): return self.board.clear_head()

    def set_and_del_head(self): return self.board.set_and_del_head(self.selected_square[0],self.selected_square[1])

    #move
    def move_sel(self,direction):
        height,width = self.board.get_board_size()
        if direction == "up":
            if self.selected_square[1]-1 >= 0:
                self.selected_square[1] = self.selected_square[1] - 1
        elif direction == "down":
            if self.selected_square[1]+1 <= height-1:
                self.selected_square[1] = self.selected_square[1] + 1
        elif direction == "left":
            if self.selected_square[0]-1 >= 0:
                self.selected_square[0] = self.selected_square[0] - 1
        elif direction == "right":
            if self.selected_square[0]+1 <= width-1:
                self.selected_square[0] = self.selected_square[0] + 1
    
    #auto set head
    def auto_set_head(self): 
        self.board.auto_set_head()
        return self.board.get_board()

    #info
    def is_head_set(self): return self.board.is_head_set()

    def get_lvl(self): return self.lvl

    def get_factor(self,x_square,y_square): return self.board.get_factor(x_square,y_square)
                
    def get_board(self): return self.board.get_board().copy()

    def get_board_size(self): return self.board.get_board_size()

    def get_wall_coordinate(self): return self.board.get_wall_coordinate()

    def get_head_coordinate(self): return self.board.get_head_coordinate()