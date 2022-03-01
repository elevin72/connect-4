from player import Player
from board import Board


class ConsolePlayer(Player):
    def __init__(self, turn):
        super().__init__(turn)
            
    def play(self, board: Board) -> Board:
        move = int(input("Please enter 1-7: ", end=""))
        while not board.is_legal_move(move):
            move = int(input("Move was not legal, try again: ", end=""))
        return board.play(move)

            

        

