import pokemon_move
import importlib
from pathlib import Path
from logger import get_logger

class PokemonFileReader:
    def __init__(self):
        self.types = set()
        self.moves = dict()
        self.logger = get_logger(__name__)

    def read_all_types(self):
        if Path("pokemon_standard_types.txt").exists():
            with open("pokemon_standard_types.txt", 'r') as file:
                for line in file:
                    self.types.add(line.strip())

            self.logger.info("Imported standard types from file")
        else:
            self.logger.error("Cannot locate standard types file, pokemon_standard_types.txt, did not import any types")
            return self.types

        if Path("pokemon_custom_types.txt").exists():
            with open("pokemon_custom_types.txt", 'r') as file:
                for line in file:
                    self.types.add(line.strip())

            self.logger.info("Imported custom types from file")
        else:
            self.logger.info("Cannot locate custom types file, pokemon_custom_types.txt, did not import any custom types")

        return self.types