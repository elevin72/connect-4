from __future__ import annotations
from typing import Set, List
from collections import namedtuple
from enum import Enum
import math
import random

WIDTH = 7
HEIGHT = 6


FOURS = [
        'XXXX',
        'OOOO'
        ]

THREES = [
        ' XXX',
        'X XX',
        'XX X',
        'XXX ',

        ' OOO',
        'O OO',
        'OO O',
        'OOO '
        ]

MINOR_COMBOS = {
        'XX  ':  5,
        ' XX ':  5,
        '  XX':  5,
        'X X ':  5,
        ' X X':  5,
        'X  X':  5,
        'X   ':  1,
        ' X  ':  1,
        '  X ':  1,
        '   X':  1,

        'OO  ':  -5,
        ' OO ':  -5,
        '  OO':  -5,
        'O O ':  -5,
        ' O O':  -5,
        'O  O':  -5,
        'O   ':  -1,
        ' O  ':  -1,
        '  O ':  -1,
        '   O':  -1,
        }


Index = namedtuple('Index', 'row col')

class EndState(Enum):
    NOT_DONE = 0
    O_WIN = 1
    X_WIN = 2
    TIE = 3


class Threat:
    def __init__(self, index: Index, turn: str):
        self.idx: Index = index
        self.turn: str = turn
    
    def is_one_away(self, other) -> bool:
        return abs(self.idx.row - other.idx.row) == 1 and self.idx.col == other.idx.col

    def __eq__(self, o: object) -> bool:
        return self.idx == o.idx and self.turn == o.turn

    def __hash__(self) -> int:
        return hash(self.idx.row) + hash(self.idx.col) + hash(self.turn)


POSITIVE = 1
NEGATIVE = -1
EVEN = 0
ODD = 1

X_WIN = 10**8
O_WIN = -X_WIN
    
class Board:

    def __init__(self, board=None, turn=None, prev_move=-1):
        self.board: List[str] = board or [' '*WIDTH for _ in range(HEIGHT)]
        self.turn: str = turn or 'X'
        self.prev_move: int = prev_move

        # end_state, x_threats and o_threats are all set(filled) in preliminiary_evaluation()
        self.end_state: EndState = EndState.NOT_DONE
        self.x_threats: Set[Threat] = set()
        self.o_threats: Set[Threat] = set()

        self._value = self.preliminary_evaluation()

    def __repr__(self) -> str:
        ret = ""
        ret += "\n" + self.turn + " to play\n"
        for i,row in enumerate(self.board):
            ret += str(HEIGHT-i)
            for spot in row:
                ret += "|" + spot
            ret += "|\n"
        ret += "  1 2 3 4 5 6 7\n\n"
        return ret

    
    def print(self):
        print("\n" + self.turn + " to play")
        for i,row in enumerate(self.board):
            print(str(HEIGHT-i), end="")
            for spot in row:
                print("|" + spot, end="")
            print("|")
        print("  1 2 3 4 5 6 7\n")
        self._print()


    def _print(self):
        print("b = Board(")
        print("       ['" + self.board[0] + "',")
        print("        '" + self.board[1] + "',")
        print("        '" + self.board[2] + "',")
        print("        '" + self.board[3] + "',")
        print("        '" + self.board[4] + "',")
        print("        '" + self.board[5] + "'],")
        print("        '" + self.turn + "')")

    def is_legal_move(self, col) -> bool:
        return self.board[0][col] == ' '

    def play(self, col: int) -> Board:
        if not self.is_legal_move(col):
            print("Move: " + str(col))
            raise RuntimeError("Move is not legal")
        for i in range(len(self.board)):
            if i == HEIGHT-1 or self.board[i + 1][col] != ' ':
                board = self.board.copy()
                board[i] = self.board[i][:col] + self.turn + self.board[i][col+1:]
                if self.turn == 'X':
                    turn = 'O'
                else:
                    turn = 'X'
                return Board(board=board, turn=turn, prev_move=col)

    def get_next_states(self) -> List[Board]:
        next_states = []
        for i in range(WIDTH):
            if self.is_legal_move(i):
                next_states.append(self.play(i))
        if next_states == []:
            self.end_state = EndState.TIE
        random.shuffle(next_states)
        return next_states

    def game_over(self):
        return self.end_state != EndState.NOT_DONE

    def preliminary_evaluation(self):
        value = 0

        # horizontals
        for i in range(HEIGHT):
            value += self._value_and_threats([Index(i,j) for j in range(WIDTH)])

        # vertical
        for j in range(WIDTH):
            value += self._value_and_threats([Index(i,j) for i in range(HEIGHT)])

        # diagonal top-left to bottom-right
        for i in range(4):
            value += self._value_and_threats(self.get_primary_diagonal(Index(0,i)))
        for i in range(1,3):
            value += self._value_and_threats(self.get_primary_diagonal(Index(i,0)))

        # diagonal top-right to bottom-left
        for i in range(3,7):
            value += self._value_and_threats(self.get_secondary_diagonal(Index(0,i)))
        for i in range(1,3):
            value += self._value_and_threats(self.get_secondary_diagonal(Index(i,6)))

        if self.end_state == EndState.NOT_DONE and self.check_for_tie():
            return 0

        return value

    def check_for_tie(self):
        if self.board[0].count(' ') == 0:
            self.end_state = EndState.TIE
            return True
        return False

    def _value_and_threats(self, indices: list[Index]) -> int:
        line = self._stringify(indices)
        value = 0
        for combo in FOURS:
            if combo in line:
                if 'X' in combo:
                    self.end_state = EndState.X_WIN
                    value = X_WIN
                else: # 'O' in combo:
                    self.end_state = EndState.O_WIN
                    value = -X_WIN
        for combo in THREES:
            if combo in line:
                """ Get index that contains threat"""
                index = indices[line.index(combo) + combo.index(' ')]
                if 'X' in combo:
                    self.x_threats.add(Threat(index, 'X'))
                else:
                    self.o_threats.add(Threat(index, 'O'))
        for combo in MINOR_COMBOS:
            if combo in line:
                value += MINOR_COMBOS[combo]

        return value

    # Take a list of Indices and return a string containing their values on the current board
    def _stringify(self, indices: list[Index]) -> str:
        ret = ""
        for index in indices:
            ret += self.board[index.row][index.col]
        return ret

    def evaluate(self) -> int:
        """ looks at threats on board and assigns value based on
            - how many there are
            - where they are in relation to each other
            - where they are in relation to parity of player
            """
        value = self._value
        value += self._count_threats(self.x_threats, POSITIVE)
        value += self._count_threats(self.o_threats, NEGATIVE)
        value += self._check_threats_immediacy(self.x_threats, POSITIVE)
        value += self._check_threats_immediacy(self.o_threats, NEGATIVE)
        # value += self._check_threats_parity(self.x_threats, ODD, POSITIVE)
        # value += self._check_threats_parity(self.o_threats, EVEN, POSITIVE)
        value += self._check_threats_parity2()

        return value

    @staticmethod
    def _count_threats(threats: set[Threat], factor) -> int:
        """ Get points for every threat, 50 points per row (going down), """
        return sum(50 * factor * (t.idx.row + 1) for t in threats)

    def _check_threats_immediacy(self, threats: set[Threat], factor) -> int:
        """ Checks if threats are:
            1 immediate (are playable next turn)
            2 stacked (one on top another)
            3 immediate and stacked (one is immediate and other is on top of it)

            1 is winning if more than one threat is found
            2 is just good
            3 is immediately winning."""
        immediates = set()
        value = 0
        for t1 in threats:
            if t1.idx.row == HEIGHT - 1 or self.board[t1.idx.row + 1][t1.idx.col] != ' ':
                if t1.turn == self.turn:
                    return 10_000 * factor
                immediates.add(t1)
            if len(immediates) > 1:
                return 10_000 * factor
            for t2 in threats:
                if t1.is_one_away(t2):
                    if t1 in immediates:
                        return 10_000 * factor
                    value += 100 * factor
        return value

    @staticmethod
    def _check_threats_parity(threats: set[Threat], parity, factor) -> int:
        """ adds points if a threat is found in that players parity """
        value = 0
        for threat in threats:
            if threat.idx.row % 2 == parity:
                value += 1000 * factor 
        return value

    def _check_threats_parity2(self) -> int:
        def under(threat: Threat, other_threats: Set[Threat]) -> bool:
            for other_threat in other_threats:
                if threat.idx.col == other_threat.idx.col and threat.idx.row < other_threat.idx.row:
                    return True
            return False

        x_odd_threats = {threat for threat in self.x_threats if threat.idx.row % 2 == 1}
        # x_even_threats = {threat for threat in self.x_threats if threat.idx.row % 2 == 0}
        o_odd_threats = {threat for threat in self.o_threats if threat.idx.row % 2 == 1}
        o_even_threats = {threat for threat in self.o_threats if threat.idx.row % 2 == 0}

        x_odd_threats = {x_threat for x_threat in x_odd_threats if under(x_threat, o_even_threats)}
        o_even_threats = {o_threat for o_threat in o_even_threats if under(o_threat, x_odd_threats)}

        # X
        for x_threat in x_odd_threats:
            if all(o_threat.idx.col != x_threat.idx.col for o_threat in o_odd_threats):
                # good for X
                return 1000
        if len(x_odd_threats) - len(o_odd_threats) == 1:
            # good for X
            return 1000
        if len(x_odd_threats) == 3:
            # good for X
            return 1000
        
        # O
        if len(o_even_threats) == 1 and len(x_odd_threats) == 0:
            # good for o
            return -1000
        if len(o_odd_threats) == 2:
            o_odd_threat_cols = {o_threat.idx.col for o_threat in o_odd_threats}
            x_odd_threat_cols = {x_threat.idx.col for x_threat in x_odd_threats}
            if all(x_col in o_odd_threat_cols for x_col in x_odd_threat_cols):
                # good for o
                return -1000
        return 0

    def get_column(self, i) -> list[tuple(int,int)]:
        ret = []
        for j in range(self.board):
            ret.append((i,j))
        return ret
            
    def get_primary_diagonal(self, index: Index) -> list[Index]:
        ret = []
        while index.row != -1 and index.col != -1 and index.row != HEIGHT and index.col != WIDTH:
            ret.append(index)
            index = Index(index.row + 1, index.col + 1)
        return ret

    def get_secondary_diagonal(self, index: Index) -> list[tuple(int,int)]:
        ret = []
        while index.row != -1 and index.col != -1 and index.row != HEIGHT and index.col != WIDTH:
            ret.append(index)
            index = Index(index.row + 1, index.col - 1)
        return ret
