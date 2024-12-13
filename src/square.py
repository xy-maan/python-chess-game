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
    
    def has_rival_piece(self, color):
        return self.piece.color != color
    
    def empty_or_rival(self, color):
        return self.is_empty() or self.has_rival_piece(color)