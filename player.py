class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return '(' + str(self.x) + ', ' + str(self.y) + ')'

    def __add__(self, other):
        return Position(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Position(self.x - other.x, self.y - other.y)


# TODO: add options
class Player:
    def __init__(self,
                 is_knight: bool,
                 was_knight: bool,
                 blanks: int,
                 trace: list,
                 name: str,
                 colour: str,
                 is_alive=True):
        self.is_knight = is_knight
        self.was_knight = was_knight
        self.blanks = blanks
        self.trace = trace
        self.name = name
        self.colour = colour
        self.is_alive = is_alive

    def get_trace(self):
        return self.trace

    # def get_is_knight(self):
    #     return self.is_knight

    def get_blanks(self):
        return self.blanks

    # def get_name(self):
    #     return self.name

    def next_position(self, new_pos):
        self.trace.append(new_pos)

    def cancel_move(self):
        self.trace.pop()

    def reduce_blanks(self):
        self.blanks -= 1

    def kill(self):
        pass
