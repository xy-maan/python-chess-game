class Square:

    # row and col are coordinates
    def __init__(self, row, col, piece=None):
        self.row = row
        self.col = col
        self.piece = piece

    # check does it has a piece so that we can render it.
    def has_piece(self):
        return self.piece != None