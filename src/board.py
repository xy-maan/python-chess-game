from square import Square
from const import *
from piece import *
from move import Move


class Board:

    def __init__(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for _ in range(COLS)]
        self.last_move = None
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

    # move is a Move() object
    def move(self, piece, move):

        # get move coordianates
        initial = move.initial
        final = move.final


        # updating the board

        # remove the piece form the old square.
        self.squares[initial.row][initial.col].piece = None

        # put the piece on the new square.
        self.squares[final.row][final.col].piece = piece

        # pawn promotion
        if isinstance(piece, Pawn):
            self.check_promotion(piece, final)

        piece.moved = True

        # clear all the valid moves (highlighted squares), since we changed the position.
        piece.moves = []

        self.last_move = move

    def valid_move(self, piece, move):

        # we need to implement the __eq__ method inside move.py to let python know how to compare them, since they are self made objects.
        return move in piece.moves

    def check_promotion(self, piece, final):
        
        # has the pawn reached the final row from either side?
        if final.row == 0 or final.row == 7:
            self.squares[final.row][final.col].piece = Queen(piece.color)

    def promoted(self, piece, row):

        if isinstance(piece, Pawn) and (row == 0 or row == 7):
            return True
        
        return False

    # main valid moves calculation method
    def calc_moves(self, row, col, piece):

        if isinstance(piece, Pawn):
            self.pawn_moves(row, col, piece)
        elif isinstance(piece, Bishop):
            self.straightline_moves(row, col, piece, [(-1, 1), (-1, -1), (1, 1), (1, -1)])  # up-right  # up-left  # down-right  # down-left
        elif isinstance(piece, Knight):
            self.knight_moves(row, col, piece)
        elif isinstance(piece, Rook):
            self.straightline_moves(row, col, piece, [(-1, 0), (0, 1), (1, 0), (0, -1)])  # up  # right  # down  # left
        elif isinstance(piece, Queen):
            self.straightline_moves(
                row,
                col,
                piece,
                [
                    (-1, 0),  # up
                    (0, 1),  # right
                    (1, 0),  # down
                    (0, -1),  # left
                    (-1, 1),  # up-right
                    (-1, -1),  # up-left
                    (1, 1),  # down-right
                    (1, -1),  # down-left
                ],
            )
        elif isinstance(piece, King):
            self.king_moves(row, col, piece)

    # calculate king moves
    def king_moves(self, row, col, piece):
        adjs = [
            (row - 1, col),  # up
            (row - 1, col + 1),  # up-right
            (row, col + 1),  # right
            (row + 1, col + 1),  # down-right
            (row + 1, col),  # down
            (row + 1, col - 1),  # down-left
            (row, col - 1),  # left
            (row - 1, col - 1),  # up-left
        ]

        # normal king moves
        for adj in adjs:

            new_row, new_col = adj

            if Square.inside_board(new_row, new_col):
                if self.squares[new_row][new_col].empty_or_enemy(piece.color):
                    initial = Square(row, col)
                    final = Square(new_row, new_col)

                    move = Move(initial, final)

                    piece.add_move(move)

        # queen-side castling

        # king-side castling

    # calculate knight valid moves
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

    # calculate valid pawn moves
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

    # calculate valid moves for queen, rook and bishop
    def straightline_moves(self, row, col, piece, incrs):

        for incr in incrs:

            # save the increments
            row_incr, col_incr = incr

            # new coordinates
            new_row = row + row_incr
            new_col = col + col_incr

            while True:
                if Square.inside_board(new_row, new_col):

                    initial = Square(row, col)
                    final = Square(new_row, new_col)

                    move = Move(initial, final)

                    # the square is empty, then it's valid
                    if self.squares[new_row][new_col].is_empty():
                        piece.add_move(move)

                    # the square has an enemy piece
                    if self.squares[new_row][new_col].has_enemy_piece(piece.color):
                        piece.add_move(move)

                        # we break since it's the last point we can reach
                        break

                    # the square has a team piece, here we should break immediately
                    if self.squares[new_row][new_col].has_team_piece(piece.color):
                        break

                # not inside the board
                else:
                    break

                # add the same increment to check for other squares that are in the same direction.
                new_row += row_incr
                new_col += col_incr
