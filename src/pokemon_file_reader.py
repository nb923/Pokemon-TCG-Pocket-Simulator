import pokemon_move
import importlib
from pathlib import Path
from logger import get_logger

class PokemonFileReader:
    def __init__(self):
        self.types = set()
        self.moves = dict()
        self.logger = get_logger(__name__)