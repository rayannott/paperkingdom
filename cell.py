class Cell:
    """
    The t parameter is a string; it has a form of <character,number,extra_parameters>
    Here are some examples:
    'p4' is a player 4
    'o2' is a trace left by a player 2
    'o1u' is a trace of a player 1 that has been used in a tetra
    'x0' is a shot made by a player 0
    'n-' is an empty cell
    'w-' is a wall
    't-' is a target
    """

    def __init__(self, t):
        self.t = t

    def is_player(self):
        if self.t[0] == 'p':
            return True, int(self.t[1:])
        else:
            return False, 0

    def is_shot(self):
        if self.t[0] == 'x':
            return True, int(self.t[1:])
        else:
            return False, 0

    def is_target(self):
        if self.t[0] == 't':
            return True
        else:
            return False

    def is_trace_used(self):
        if self.t[-1] == 'u':
            return True
        else:
            return False

    def is_trace(self):
        if self.t[0] == 'o':
            return True
        else:
            return False

    def is_empty(self):
        if self.t[0] == 'n':
            return True
        else:
            return False