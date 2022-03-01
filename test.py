from abminimax import *

b = Board(
       ['       ',
        '       ',
        '   O X ',
        '  XO O ',
        '  OX X ',
        '  XO X '],
        'O')
b.evaluate()

a,b = ab_minimax(b, 2, -math.inf, math.inf, False)
b = Board(
       ['       ',
        '     O ',
        '   O X ',
        '  XO O ',
        '  OX X ',
        '  XO X '],
        'X')
b.evaluate()
a,b = ab_minimax(b, 2, -math.inf, math.inf, True)

# for _ in range(100):
#     d = ab_minimax(b, 2, -math.inf, math.inf, True)[1]
#     d.print()
