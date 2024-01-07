import json
from src.board import Board
class Play:
    def __init__(self):
        self.board = Board()

    # board
    def import_board(self,lvl):
        with open("./lib/map.json","r") as f:
            map = json.load(f)
        self.board.load_board(map[str(lvl)])

    def load_board(self,board):
        self.board.load_board(board)

    #move
    def move(self,direction):
        return self.board.move(direction)
    
    def undo_step(self):
        return self.board.undo_step()
    
    #info
    def is_win(self): 
        return self.board.is_win()
    
    def is_lose(self): 
        return self.board.is_lose()

    def get_board(self): return self.board.get_board().copy()

    def get_board_size(self): return self.board.get_board_size()

    def get_wall_coordinate(self): return self.board.get_wall_coordinate()

    def get_head_coordinate(self): return self.board.get_head_coordinate()

