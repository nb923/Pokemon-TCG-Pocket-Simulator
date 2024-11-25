import pokemon_coin
from logger import get_logger

class PokemonTCGPocketEmulator:
    def __init__(self):
        self.deck_one = []
        self.deck_two = []

        self.hand_one = []
        self.hand_two = []

        self.board_one_active = None
        self.board_one_passive = [None] * 3

        self.board_two_active = None
        self.board_two_passive = [None] * 3

        self.coin =  pokemon_coin.PokemonCoin()

        self.points_one = 0
        self.points_two = 0

        self.logger = get_logger(__name__)