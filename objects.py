# -*- coding: utf-8 -*-
import copy


class Piece(object):
    """
    A borad's piece
    """
    def __init__(self, posx=None, posy=None, board=None):
        self.board = board
        self.posx = posx
        self.posy = posy


class King(Piece):

    def __unicode__(self):
        return u'K'

    def get_possible_moves(self):
        moves = [(self.posx+1, self.posy),
                (self.posx-1, self.posy),
                (self.posx+1, self.posy+1),
                (self.posx+1, self.posy-1),
                (self.posx-1, self.posy+1),
                (self.posx-1, self.posy-1),
                (self.posx, self.posy+1),
                (self.posx, self.posy-1)]
        return [i for i in moves if i[0] >=0 and i[1] >=0 and i[0] < self.board.board_width and i[1] < self.board.board_height]


class Rook(Piece):

    def __unicode__(self):
        return u'K'

    def get_possible_moves(self):
        return [(self.posx+i, self.posy) \
                 for i in range(self.posx, self.board.board_width-1)] + \
               [(self.posx, self.posy+i) \
                 for i in range(self.posy, self.board.board_height-1)] + \
               [(self.posx-i, self.posy) \
                 for i in range(self.posx, 0, -1)] + \
               [(self.posx, self.posy-i) \
                 for i in range(self.posy, 0, -1)]


class Board(object):
    """
    A chess board
    """

    def __init__(self, board_width, board_height):
        """
        Based on width and height, create the board info.
        """
        self.board_width = board_width
        self.board_height = board_height
        self._board_data = [{u'has_piece': False, u'disabled': False} for x in range(board_width*board_height)]

    def __getitem__(self, item):
        return self._board_data[item * self.board_width: (item * self.board_width) + self.board_width]

    def enumerate(self):
        for x in range(self.board_width):
            for y in range(self.board_height):
                yield [(x, y), self[x][y]]

    def __iter__(self):
        for i in self._board_data:
            yield i

    def copy(self):
        new_board = Board(self.board_width, self.board_height)
        new_board._board_data = copy.deepcopy(self._board_data)
        return new_board


ee = Board(3, 3)
result = []
def resolve(board, pieces):
    for piece_n, piece in enumerate(pieces, 1):
        for pos_na, posa in board.enumerate():
            board2 = board.copy()
            pos_n = pos_na
            pos = board2[pos_n[0]][pos_n[1]]
            if not pos[u'disabled'] and not pos[u'has_piece']:
                pos[u'has_piece'] = True
                for move in piece(pos_n[0], pos_n[1], board2).get_possible_moves():
                    if not board2[move[0]][move[1]][u'disabled'] and not not board2[move[0]][move[1]][u'has_piece']:
                        board2[move[0]][move[1]]['disabled'] = True
                    else:
                        break
                if not pieces[piece_n:]:
                    result.append(board2)
                else:
                    resolve(board2.copy(), pieces[piece_n:])
            else:
                break


