import random

class PokemonCoin:
    def __init__(self):
        self.state = None

    def flip_coin(self):
        num = random.randint(0, 1)

        if num == 0:
            self.state = "Heads"
        else:
            self.state = "Tails"