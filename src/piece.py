import os

class Piece:

    # rpv = relative piece value
    def __init__(self, name, color, rpv, img_path=None, pos=None):
        self.name = name
        self.color = color

        value_sign = 1 if color == "white" else -1
        self.value = rpv * value_sign

        self.moves = []
        self.moved = False
        
        self.img_path = img_path
        self.set_img()
        self.pos = pos

    # we we os.path.join() for cross-platform compatibility.
    def set_img(self):
        self.img_path = os.path.join(f"../assets/{self.color}/{self.name}.png")

    def add_move(self, move):
        self.moves.append(move)


# The followig classes have pretty much the same structure, we create an instance with the piece name, the color, and its reltive value #


class Pawn(Piece):

    def __init__(self, color):
        self.dir = -1 if color == "white" else 1
        super().__init__("pawn", color, 1.0)

class Knight(Piece):

    def __init__(self, color):
        super().__init__("knight", color, 3.0)

class Bishop(Piece):

    def __init__(self, color):
        super().__init__("bishop", color, 3.0)


class Rook(Piece):

    def __init__(self, color):
        super().__init__("rook", color, 5.0)


class Queen(Piece):

    def __init__(self, color):
        super().__init__("queen", color, 9.0)

class King(Piece):

    def __init__(self, color):
        # for castling
        left_rook = None
        right_rook = None
        
        super().__init__("king", color, 10000)
