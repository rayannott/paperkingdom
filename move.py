class Move:
    # move is Position
    # shoot is Position
    # swap is Boolean
    def __init__(self, swap, move, shoot):
        self.swap = swap
        self.move = move
        self.shoot = shoot

    def get_move(self):
        return self.move

    def get_shoot(self):
        return self.shoot

    def get_swap(self):
        return self.swap
