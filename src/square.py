class Square:

    # row and col are coordinates
    def __init__(self, row, col, piece=None):
        self.row = row
        self.col = col
        self.piece = piece

    # check does it has a piece so that we can render it.
    def has_piece(self):
        return self.piece != None

    @staticmethod
    def inside_board(*args):

        for arg in args:
            if arg < 0 or arg > 7:
                return False

        return True

    def is_empty(self):
        return not self.has_piece()

    # we must check that the square has a piece before checking the piece color, pawn diagonal test problem.
    def has_enemy_piece(self, color):
        return self.has_piece() and self.piece.color != color
    
    def has_team_piece(self, color):
        return self.has_piece() and self.piece.color == color

    def empty_or_enemy(self, color):
        return self.is_empty() or self.has_enemy_piece(color)
