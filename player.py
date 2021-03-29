class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Player:
    def __init__(self, is_knight, was_knight, blanks, trace, name):
        self.is_knight = is_knight
        self.was_knight = was_knight
        self.blanks = blanks
        self.trace = trace
        self.name = name

    def get_trace(self):
        return self.trace

    def get_is_knight(self):
        return self.is_knight

    def get_blanks(self):
        return self.blanks

    def get_name(self):
        return self.name

    def next_position(self, new_pos):
        self.trace.append(new_pos)
