class PokemonAbility:
    """Holds data for a single pokemon move.

    Attributes:
        name: A string that holds ability name
        passive: A boolean that is True if ability is passive, False if it is active
        activation_condition: A function that returns True if ability can be used at the current state, else False
        usable: A boolean that is True if the ability can be used at the current state
        effect: A function that does the effect of the ability
    """

    def __init__(self):
        """Initializes the instance with default values."""
        self.name = None
        self.passive = None
        self.activation_condition = None
        self.usable = None
        self.effect = None 

    def __eq__(self, other):
        """Compares contents of self with contents of other ability.
        
        Returns:
            A boolean, True, if both ability's contents are the same, else False"""
        if not isinstance(other, PokemonAbility):
            return False
        
        return self.name == other.name and self.passive == other.passive and self.activation_condition == other.activation_condition and self.usable == other.usable and self.effect == other.effect