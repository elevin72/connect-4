from abminimax import *
from board import *

DEPTH = 2

board = Board()
# while True:
#     if board.game_over():
#         break
#     board.print()
#     if board.turn == 'X':
#         board = ab_minimax(board, 5, -math.inf, math.inf, True)[1]
#     else:
#         board = ab_minimax(board, 2, -math.inf, math.inf, False)[1]

while True:
    user = input("Select you color.\nX to go first, O to go second\n")
    if user == 'X' or user == 'O':
        break
print("Game start.\nX goes first.\nEnter a number 0-6 to drop a piece on the board.")

while True:
    if board.game_over():
        break
    board.print()
    if board.turn == user:
        move = int(input("Your turn: "))
        while not board.is_legal_move(move-1):
            move = int(input("Illegal, please try again: "))
        board = board.play(move-1)
    else:
        board = ab_minimax(board, DEPTH, -math.inf, math.inf, user == 'O')[1]

board.print()
if board.end_state == EndState.X_win:
    print("Player X won")
if board.end_state == EndState.O_win:
    print("Player O won")
if board.end_state == EndState.tie:
    print("It's a tie")
# else:
#     print("Better luck next time")
