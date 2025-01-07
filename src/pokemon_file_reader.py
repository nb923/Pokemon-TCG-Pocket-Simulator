import pokemon_move
import importlib
from pathlib import Path
from logger import get_logger

class PokemonFileReader:
    """Loads standard and custom pokemon data from files.

    Attributes:
        types: A set of allowed types.
        moves: A dictionary of allowed moves where the key is the name and the value a pokemon_move object.
        logger: A general logger passed from logger.py .
    """

    def __init__(self):
        """Initializes the instance with default values."""

        self.types = set()
        self.moves = dict()
        self.logger = get_logger(__name__)

    def read_all_types(self):
        """Reads allowed types from files.

        Reads allowed types from pokemon_standard_types.txt and pokemon_custom_types.txt 
        and stores in self.types. 
        
        - If no standard file is provided, it does not read from
        any file.
        - If no custom file is provided, but a standard file exists,
        reads only from standard.
        - If both are provided, reads from both files.

        Returns:
            A set, self.types, which stores the valid types.
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
    
    def read_all_moves(self):
        """Reads valid moves from files.
        
        Reads valid moves from pokemon_standard_moves.txt and pokemon_custom_moves.txt
        and stores in self.moves. If a file doesn't exist, or contains invalid moves,
        skips file/all invalid moves.

        Returns:
            A dictionary, self.moves, which stores move name -> pokemon_move object.
        """

        # Reads from pokemon_standard_moves.txt
        if Path("pokemon_standard_moves.txt").exists():
            with open("pokemon_standard_moves.txt", 'r') as file:
                for line in file:
                    move = self.read_move(line)

                    if move is not None:
                        self.moves[move.name] = move 

            self.logger.info("Imported standard moves from file")
        else:
            self.logger.error("Cannot locate custom moves file, pokemon_standard_moves.txt, did not import any moves")
            return dict()

        # Reads from pokemon_custom_moves.txt
        if Path("pokemon_custom_moves.txt").exists():
            with open("pokemon_custom_moves.txt", 'r') as file:
                for line in file:
                    move = self.read_move(line)

                    if move is not None:
                       self.moves[move.name] = move 

            self.logger.info("Imported custom moves from file")
        else:
            self.logger.info("Cannot locate custom moves file, pokemon_custom_moves.txt, did not import any custom moves")

        return self.moves
    
    def read_move(self, move_text):
        """Reads a move from a text string

        Reads a move from a string in the form "Move Name: [Name], Energies: [Types seperated by the delimiter '; '], 
        Damage: [Numerical Amount], Effect Function: [Name of effect function]".

        For example: "Move Name: Thunderbolt, Energies: Electric; Electric, Damage: 50, Effect Function: thunderbolt_effect".

        Effect functions will be stored in either pokemon_standard_move_effect_list.py for standard moves and
        pokemon_custom_move_effect_list.py for custom moves.

        If formatting of string is incorrect, no name is given, an illegal type is used for energy, move
        damage value isn't a number, or the effect function does not exist, then returns None.

        Args:
            move_text: A string that contains an encoded move
        
        Returns:
            A pokemon_move object that stores the move's details; None is returned if invalid input
        """

        move_elements = move_text.split(", ")

        if len(move_elements) != 4:
            self.logger.error(f"Error in formatting of move: {move_text}")
            return None

        move = pokemon_move.PokemonMove()

        # Reads move name
        move_name_split = move_elements[0].split("Move Name:")

        if len(move_name_split) != 2:
            self.logger.error(f"Error in formatting of move name for move: {move_text}")
            return None
        elif len(move_name_split[1].strip()) == 0:
            self.logger.error(f"No name is given for move: {move_text}")
            return None
        
        move.name = move_name_split[1].strip()

        # Reads move energies
        move_energy_split = move_elements[1].split("Energies:")

        if len(move_energy_split) != 2:
            self.logger.error(f"Error in formatting of move energy for move: {move_text}")
            return None

        energy_list = []

        if move_energy_split[1].strip() != "None":
            for energy in move_energy_split[1].strip().split(";"):
                energy = energy.strip()

                if energy not in self.types:
                    self.logger.error(f"Illegal energy type used in move: {move_text}")
                    return None
                
                energy_list.append(energy)

        move.energy = energy_list

        # Reads move damage
        move_damage_split = move_elements[2].split("Damage:")

        if len(move_damage_split) != 2:
            self.logger.error(f"Error in formatting of move damage for move: {move_text}")
            return None
        elif not move_damage_split[1].strip().isdigit():
            self.logger.error(f"Move damage value is not digit for move: {move_text}")
            return None

        move.damage = int(move_damage_split[1].strip())

        # Reads move effect
        move_effect_split = move_elements[3].split("Effect Function:")

        if len(move_effect_split) != 2:
            self.logger.error(f"Error in formatting of move function for move: {move_text}")
            return None
        elif move_effect_split[1].strip() == "None":
            move.effect = None
            return move
        
        standard_function_list = None
        custom_function_list = None
        
        standard_exists = False
        custom_exists = False
        
        if Path.exists("pokemon_standard_move_effect_list.py"):
            standard_function_list = importlib.import_module("pokemon_standard_move_effect_list")
            standard_exists = True
       
        if Path.exists("pokemon_custom_move_effect_list.py"):
            custom_function_list = importlib.import_module("pokemon_custom_move_effect_list")
            custom_exists = True

        if not (standard_exists or custom_exists):
            self.logger.error("Move effect modules are not present")
            return None
        
        if standard_exists and move_effect_split[1].strip() in dir(standard_function_list):
            move.effect = getattr(standard_function_list, move_effect_split[1].strip())
        elif custom_exists and move_effect_split[1].strip() in dir(custom_function_list):
            move.effect = getattr(custom_function_list, move_effect_split[1].strip())
        else:
            self.logger.error(f"Move effect function does not exist for move: {move_text}")
            return None

        return move