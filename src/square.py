class Square:

    ALPHA_COLS = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h"}

    # row and col are coordinates
    def __init__(self, row, col, piece=None):
        self.row = row
        self.col = col
        self.piece = piece
        self.alph_col = self.ALPHA_COLS[col]

    def __eq__(self, other):
        return self.row == other.row and self.col == other.col

    # check does it has a piece so that we can render it.
    def has_piece(self):
        return self.piece != None

    @staticmethod
    def inside_board(*args):

        for arg in args:
            if arg < 0 or arg > 7:
                return False

        return True

    @staticmethod
    def get_alpha(col):
        ALPHA_COLS = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h"}
        return ALPHA_COLS[col]

    def is_empty(self):
        return not self.has_piece()

    # we must check that the square has a piece before checking the piece color, pawn diagonal test problem.
    def has_enemy_piece(self, color):
        return self.has_piece() and self.piece.color != color

    def has_team_piece(self, color):
        return self.has_piece() and self.piece.color == color

    def empty_or_enemy(self, color):
        return self.is_empty() or self.has_enemy_piece(color)
