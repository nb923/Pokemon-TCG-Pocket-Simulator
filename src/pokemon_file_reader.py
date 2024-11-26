import pokemon_move
import importlib
from pathlib import Path
from logger import get_logger

class PokemonFileReader:
    """Loads standard and custom pokemon data from files.

    Attributes:
        types: A set of allowed types.
        moves: A dictionary of allowed moves where the key is the name and the value a pokemon_move object
        logger: A general logger passed from logger.py 
    """

    def __init__(self):
        """Initializes the instance with default values"""
        
        self.types = set()
        self.moves = dict()
        self.logger = get_logger(__name__)

    def read_all_types(self):
        """Reads allowed types from files

        Reads allowed types from pokemon_standard_types.txt and pokemon_custom_types.txt 
        and stores in self.types. 
        
        - If no standard file is provided, it does not read from
        any file
        - If no custom file is provided, but a standard file exists,
        reads only from standard
        - If both are provided, reads from both files

        Returns:
            A set, self.types, which stores the valid types
        """

        # Reads from pokemon_standard_types.txt
        if Path("pokemon_standard_types.txt").exists():
            with open("pokemon_standard_types.txt", 'r') as file:
                for line in file:
                    self.types.add(line.strip())

            self.logger.info("Imported standard types from file")
        else:
            self.logger.error("Cannot locate standard types file, pokemon_standard_types.txt, did not import any types")
            return self.types

        # Reads from pokemon_custom_types.txt
        if Path("pokemon_custom_types.txt").exists():
            with open("pokemon_custom_types.txt", 'r') as file:
                for line in file:
                    self.types.add(line.strip())

            self.logger.info("Imported custom types from file")
        else:
            self.logger.info("Cannot locate custom types file, pokemon_custom_types.txt, did not import any custom types")

        return self.types