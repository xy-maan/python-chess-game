from color import Color


class Theme:

    def __init__(self, light_square, dark_square, last_move_light, last_move_dark, valid_move_light, valid_move_dark):

        self.square_color = Color(light_square, dark_square)
        self.last_move = Color(last_move_light, last_move_dark)
        self.valid_move = Color(valid_move_light, valid_move_dark)
