from square import Square
from const import *
from piece import *
from move import Move
import copy

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

        # castling
        if isinstance(piece, King):
            # if it's a castling move
            if self.castling(initial, final):
                # to determine if it's king-side or queen-side castling.
                diff = final.col - initial.col

                # pick up the rook that we're going to castle with
                rook = piece.left_rook if diff < 0 else piece.right_rook

                # move the rook, then get back here and move the king
                self.move(rook, rook.moves[-1])

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

    # if the king can move 2 squares, this means we can castle.
    def castling(self, initial, final):
        return abs(initial.col - final.col) == 2

    def castled(self, piece, initial, final):
        return isinstance(piece, King) and abs(initial.col - final.col) == 2

    # main valid moves calculation method
    def calc_moves(self, row, col, piece, flag=True):

        if isinstance(piece, Pawn):
            self.pawn_moves(row, col, piece, flag)
        elif isinstance(piece, Bishop):
            self.straightline_moves(row, col, piece, [(-1, 1), (-1, -1), (1, 1), (1, -1)], flag)  # up-right  # up-left  # down-right  # down-left
        elif isinstance(piece, Knight):
            self.knight_moves(row, col, piece, flag)
        elif isinstance(piece, Rook):
            self.straightline_moves(row, col, piece, [(-1, 0), (0, 1), (1, 0), (0, -1)], flag)  # up  # right  # down  # left
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
                flag
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
        if not piece.moved: # the king hasn't moved.
            left_rook = self.squares[row][0].piece

            # if there's a rook on the rook square
            if isinstance(left_rook, Rook):
                # the rook hasn't moved, just as the king
                if not left_rook.moved:
                    for c in range(1, 4):
                        # castling is not possible, because there's a piece in between.
                        if self.squares[row][c].has_piece():
                            break

                        # there are no pieces in between.
                        if c == 3:
                            # add left rook to our king
                            piece.left_rook = left_rook

                            # rook move
                            initial = Square(row, 0)
                            final = Square(row, 3)

                            move = Move(initial, final)
                            left_rook.add_move(move)

                            # king move
                            initial = Square(row, col)
                            final = Square(row, 2)

                            move = Move(initial, final)
                            piece.add_move(move)

        # king-side castling
        if not piece.moved:  # the king hasn't moved.
            right_rook = self.squares[row][7].piece

            # if there's a rook on the rook square
            if isinstance(right_rook, Rook):
                # the rook hasn't moved, just as the king
                if not right_rook.moved:
                    for c in range(5, 7):
                        # castling is not possible, because there's a piece in between.
                        if self.squares[row][c].has_piece():
                            break

                        # there are no pieces in between.
                        if c == 6:
                            # add left rook to our king
                            piece.right_rook = right_rook

                            # rook move
                            initial = Square(row, 7)
                            final = Square(row, 5)

                            move = Move(initial, final)
                            right_rook.add_move(move)

                            # king move
                            initial = Square(row, col)
                            final = Square(row, 6)

                            move = Move(initial, final)
                            piece.add_move(move)

    # calculate knight valid moves
    def knight_moves(self, row, col, piece, flag=True):

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

                    # save the final piece to determine if it's the king of the opponent (check)
                    final_piece = self.squares[new_row][new_col].piece

                    initial = Square(row, col)
                    final = Square(new_row, new_col, final_piece)

                    move = Move(initial, final)

                    piece.add_move(move)

    # calculate valid pawn moves
    def pawn_moves(self, row, col, piece, flag=True):

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

            # called from main, need to calculate potential checks
            if flag:

                # check potential checks, and it should be safe to add the move.
                if not self.in_check(piece, move):
                    piece.add_move(move)
                
            else:
                # called from in_check calculating opponent valid moves.
                piece.add_move(move)

        # diagonal moves
        new_row = row + piece.dir
        new_cols = [col + 1, col - 1]

        for new_col in new_cols:
            if Square.inside_board(new_row, new_col):
                if self.squares[new_row][new_col].has_enemy_piece(piece.color):

                    # save the final piece to determine if it's the king of the opponent (check)
                    final_piece = self.squares[new_row][new_col].piece

                    initial = Square(row, col)
                    final = Square(new_row, new_col, final_piece)

                    move = Move(initial, final)

                    piece.add_move(move)

    # calculate valid moves for queen, rook and bishop
    def straightline_moves(self, row, col, piece, incrs, flag=True):

        for incr in incrs:

            # save the increments
            row_incr, col_incr = incr

            # new coordinates
            new_row = row + row_incr
            new_col = col + col_incr

            while True:
                if Square.inside_board(new_row, new_col):

                    # save the final piece to determine if it's the king of the opponent (check)
                    final_piece = self.squares[new_row][new_col].piece

                    initial = Square(row, col)
                    final = Square(new_row, new_col, final_piece)


                    move = Move(initial, final)

                    # the square is empty, then it's valid
                    if self.squares[new_row][new_col].is_empty():
                        piece.add_move(move)

                    # the square has an enemy piece
                    elif self.squares[new_row][new_col].has_enemy_piece(piece.color):
                        piece.add_move(move)

                        # we break since it's the last point we can reach
                        break

                    # the square has a team piece, here we should break immediately
                    elif self.squares[new_row][new_col].has_team_piece(piece.color):
                        break

                # not inside the board
                else:
                    break

                # add the same increment to check for other squares that are in the same direction.
                new_row += row_incr
                new_col += col_incr

    def in_check(self, piece, move):
        temp_piece = copy.deepcopy(piece)
        temp_board = copy.deepcopy(self)

        # attempt the move on the temporary board.
        temp_board.move(temp_piece, move)

        # loop all squares and check for all enemy pieces and calculate their valid moves, in order to see if one of their valid moves reach our king.
        for row in range(ROWS):
            for col in range(COLS):
                if temp_board.squares[row][col].has_enemy_piece(piece.color):
                    enemy_piece = temp_board.squares[row][col].piece

                    # print(f"{enemy_piece.name} is at {row, col}")

                    # calculate the moves for the opponent.
                    temp_board.calc_moves(enemy_piece, row, col, flag=False)

                    for move in enemy_piece.moves:
                        # check if the final square has our king or not.
                        if isinstance(move.final.piece, King):
                            return True

        return False
