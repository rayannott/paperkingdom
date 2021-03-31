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

    def __init__(self, cell_type, owner_id, parameter=False):
        # string representation
        self.t = t
        self.cell_type = cell_type  # int: player - 1, trace - 2, shot - 3, target - 4, wall - 5
        self.owner_id = owner_id
        self.parameter = parameter

        self.player = cell_type == 1
        self.trace = cell_type == 2
        self.shot = cell_type == 3
        self.target = cell_type == 4
        self.wall = cell_type == 5
        self.empty = cell_type == 0

    def __str__(self):
        types = ['n', 'p', 'o', 'x', 't', 'w']
        res = types[self.cell_type]
        if self.player or self.trace or self.shot:
            res += str(self.cell_type)
        else:
            res += '-'
        if self.trace:
            res += str('u')
        pass

    def is_player(self):
        return self.player

    def is_shot(self):
        return self.shot

    def is_target(self):
        return self.target

    def is_trace(self):
        return self.trace

    def is_empty(self):
        return self.empty

    def is_trace_used(self):
        return self.parameter
