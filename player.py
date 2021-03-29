class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Player:
    def __init__(self, is_knight, was_knight, blanks, trace):
        self.is_knight = is_knight
        self.was_knight = was_knight
        self.blanks = blanks
        self.trace = trace
