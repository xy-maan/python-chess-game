class Move:

    # initial and final are Square() objects.
    def __init__(self, initial, final):
        self.initial = initial
        self.final = final

    # __eq__ is a dunder method, and it's just like a compare function in C++.
    def __eq__(self, other):

        # same here, we need to do the same in square.py since initial and final are Square() objects.
        return self.initial == other.initial and self.final == other.final