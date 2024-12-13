from square import Square
from const import *
from piece import *
from move import Move


class Board:

    def __init__(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for _ in range(COLS)]
        self._create()
        self._add_pieces("white")
        self._add_pieces("black")

    # initialize the squres with coordinates.
    def _create(self):
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)

    # assign each square its piece (at game start).
    def _add_pieces(self, color):
        row_pawn, row_other = (6, 7) if color == "white" else (1, 0)

        # Pawns
        for col in range(COLS):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))

        # Bishops
        self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
        self.squares[row_other][5] = Square(row_other, 5, Bishop(color))

        # Knights
        self.squares[row_other][1] = Square(row_other, 1, Knight(color))
        self.squares[row_other][6] = Square(row_other, 6, Knight(color))

        # Rooks
        self.squares[row_other][0] = Square(row_other, 0, Rook(color))
        self.squares[row_other][7] = Square(row_other, 7, Rook(color))

        # Queen
        self.squares[row_other][3] = Square(row_other, 3, Queen(color))

        # King
        self.squares[row_other][4] = Square(row_other, 4, King(color))

    def calc_moves(self, row, col, piece):

        if isinstance(piece, Pawn):
            self.pawn_moves(row, col, piece)
        elif isinstance(piece, Bishop):
            pass
        elif isinstance(piece, Knight):
            self.knight_moves(row, col, piece)
        elif isinstance(piece, Rook):
            pass
        elif isinstance(piece, Queen):
            pass
        elif isinstance(piece, King):
            pass

    def knight_moves(self, row, col, piece):

        # all the moves a knight can make being on any square.
        moves = [
            (row + 1, col + 2),
            (row + 1, col - 2),
            (row - 1, col + 2),
            (row - 1, col - 2),
            (row + 2, col + 1),
            (row + 2, col - 1),
            (row - 2, col + 1),
            (row - 2, col - 1),
        ]

        for move in moves:
            new_row, new_col = move

            if Square.inside_board(new_row, new_col):
                if self.squares[new_row][new_col].empty_or_enemy(piece.color):

                    initial = Square(row, col)
                    final = Square(new_row, new_col)

                    move = Move(initial, final)

                    piece.add_move(move)

    def pawn_moves(self, row, col, piece):

        # a pawn can move 2 squares on the first move, otherwise, it moves 1 square.
        steps = 1 if piece.moved == True else 2

        # vertical moves
        start = row + piece.dir  # start from the first valid square
        end = row + (piece.dir * (steps + 1))  # end at the last valid square + 1 (for looping)

        # here move hold a row index, pawns move through rows.
        for move in range(start, end, piece.dir):

            # squares are out of board, or pawn is blocked by a piece.
            if not Square.inside_board(move) or not self.squares[move][col].is_empty():
                break

            # create initial and final sqaures.
            initial = Square(row, col)
            final = Square(move, col)

            move = Move(initial, final)

            piece.add_move(move)

        # diagonal moves
        new_row = row + piece.dir
        new_cols = [col + 1, col - 1]

        for new_col in new_cols:
            if Square.inside_board(new_row, new_col):
                if self.squares[new_row][new_col].has_enemy_piece(piece.color):
                    initial = Square(row, col)
                    final = Square(new_row, new_col)

                    move = Move(initial, final)

                    piece.add_move(move)
