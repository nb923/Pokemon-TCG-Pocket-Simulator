import pokemon_move
import pokemon_ability
import importlib
from pathlib import Path
from logger import get_logger

class PokemonFileReader:
    """Loads standard and custom pokemon data from files.

    Attributes:
        types: A set of allowed types.
        moves: A dictionary of allowed moves where the key is the name and the value a pokemon_move object.
        logger: A general logger passed from logger.py.
    """

    def __init__(self):
        """Initializes the instance with default values."""

        self.types = set()
        self.moves = dict()
        self.abilities = dict()
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
            self.logger.error("Cannot locate standard moves file, pokemon_standard_moves.txt, did not import any moves")
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

    def read_all_abilities(self):
        """Reads valid abilities from files.
        
        Reads valid abilities from pokemon_standard_abilities.txt and pokemon_custom_abilities.txt
        and stores in self.abilities. If a file doesn't exist, or contains invalid abilities,
        skips file/all invalid abilities.

        Returns:
            A dictionary, self.abilities, which stores ability name -> pokemon_ability object.
        """

        # Reads from pokemon_standard_abilities.txt
        if Path("pokemon_standard_abilities.txt").exists():
            with open("pokemon_standard_abilities.txt", 'r') as file:
                for line in file:
                    ability = self.read_ability(line)

                    if ability is not None:
                        self.abilities[ability.name] = ability 

            self.logger.info("Imported standard abilities from file")
        else:
            self.logger.error("Cannot locate standard abilities file, pokemon_standard_abilities.txt, did not import any abilities")
            return dict()

        # Reads from pokemon_custom_abilities.txt
        if Path("pokemon_custom_abilities.txt").exists():
            with open("pokemon_custom_abilities.txt", 'r') as file:
                for line in file:
                    ability = self.read_ability(line)

                    if ability is not None:
                       self.abilities[ability.name] = ability 

            self.logger.info("Imported custom abilities from file")
        else:
            self.logger.info("Cannot locate custom abilities file, pokemon_custom_abilities.txt, did not import any custom abilities")

        return self.abilities

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
    
    def read_ability(self, ability_text):
        """Reads an ability from a text string.

        Reads a ability from a string in the form "Ability Name: [Name], Type: [Active or Passive], Activation Function: [Name of Activation Function], Effect Function: [Name of Effect Function]".

        For example: "Ability Name: Wash Out, Type: Active, Activation Function: wash_out_activation, Effect Function: wash_out_effect".

        Activation functions will be stored in either pokemon_standard_ability_activation_list.py for standard abilities and
        pokemon_custom_ability_activation_list.py for custom abilities.

        Effect functions will be stored in either pokemon_standard_ability_effect_list.py for standard abilities and
        pokemon_custom_ability_effect_list.py for custom abilities.

        If formatting of string is incorrect, no name is given, the type is not Active or Passive, or the activation or 
        effect function does not exist, then returns None.

        Args:
            ability_text: A string that contains an encoded ability.
        
        Returns:
            A pokemon_ability object that stores the ability's details; None is returned if invalid input.
        """

        ability_elements = ability_text.split(", ")

        if len(ability_elements) != 4:
            self.logger.error(f"Error in formatting of ability: {ability_text}")
            return None

        ability = pokemon_ability.PokemonAbility()

        ability.usable = False

        # Reads ability name
        ability_name_split = ability_elements[0].split("Ability Name:")

        if len(ability_name_split) != 2:
            self.logger.error(f"Error in formatting of ability name for ability: {ability_text}")
            return None
        elif len(ability_name_split[1].strip()) == 0:
            self.logger.error(f"No name is given for ability: {ability_text}")
            return None
        
        ability.name = ability_name_split[1].strip()

        # Reads ability type
        ability_type_split = ability_elements[1].split("Type:")

        if len(ability_type_split) != 2:
            self.logger.error(f"Error in formatting of ability type for ability: {ability_text}")
            return None
        elif ability_type_split[1].strip().lower() not in ("passive", "active"):
            self.logger.error(f"Type value for ability is not passive or active in ability: {ability_text}")
            return None

        ability.passive = True if ability_type_split[1].strip().lower() == "passive" else False

        # Reads ability activation function
        ability_activation_split = ability_elements[2].split("Activation Function:")

        if len(ability_activation_split) != 2:
            self.logger.error(f"Error in formatting of ability activation function for ability: {ability_text}")
            return None
        elif ability_activation_split[1].strip() == "None":
            ability.activation_condition = None
        else:
            standard_function_list = None
            custom_function_list = None
            
            standard_exists = False
            custom_exists = False
            
            if Path.exists("pokemon_standard_ability_activation_list.py"):
                standard_function_list = importlib.import_module("pokemon_standard_ability_activation_list")
                standard_exists = True
        
            if Path.exists("pokemon_custom_ability_activation_list.py"):
                custom_function_list = importlib.import_module("pokemon_custom_ability_activation_list")
                custom_exists = True
            
            if standard_exists and ability_activation_split[1].strip() in dir(standard_function_list):
                ability.activation_condition = getattr(standard_function_list, ability_activation_split[1].strip())
            elif custom_exists and ability_activation_split[1].strip() in dir(custom_function_list):
                ability.activation_condition = getattr(custom_function_list, ability_activation_split[1].strip())
            else:
                self.logger.error(f"Ability activation function does not exist for ability: {ability_text}")
                return None

        # Reads ability effect
        ability_effect_split = ability_elements[3].split("Effect Function:")

        if len(ability_effect_split) != 2:
            self.logger.error(f"Error in formatting of ability effect function for ability: {ability_text}")
            return None
        elif ability_effect_split[1].strip() == "None":
            ability.effect = None
            return ability
        
        standard_function_list = None
        custom_function_list = None
        
        standard_exists = False
        custom_exists = False
        
        if Path.exists("pokemon_standard_ability_effect_list.py"):
            standard_function_list = importlib.import_module("pokemon_standard_ability_effect_list")
            standard_exists = True
       
        if Path.exists("pokemon_custom_ability_effect_list.py"):
            custom_function_list = importlib.import_module("pokemon_custom_ability_effect_list")
            custom_exists = True
        
        if standard_exists and ability_effect_split[1].strip() in dir(standard_function_list):
            ability.effect = getattr(standard_function_list, ability_effect_split[1].strip())
        elif custom_exists and ability_effect_split[1].strip() in dir(custom_function_list):
            ability.effect = getattr(custom_function_list, ability_effect_split[1].strip())
        else:
            self.logger.error(f"Ability effect function does not exist for ability: {ability_text}")
            return None

        return ability