
from player import *
from abminimax import *


class AiPlayer(Player):

    def __init__(self, depth, color):
        super().__init__(color)
        self.depth = depth
        
    def play(self, board: Board) -> Board:
        return ab_minimax(board, self.depth, -math.inf, math.inf, self.color == 'X')
