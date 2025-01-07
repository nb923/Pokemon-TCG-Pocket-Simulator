class PokemonMove:
    """Holds data for a single pokemon move.

    Attributes:
        name: A string that holds move name
        energy: A list that lists required energy types
        damage: An int that holds damage value of move
        effect: A function that does the effect of the move
    """

    def __init__(self):
        """Initializes the instance with default values."""
        self.name = None
        self.energy = []
        self.damage = None
        self.effect = None

    def __eq__(self, other):
        """Compares contents of self with contents of other move.
        
        Returns:
            A boolean, True, if both move's contents are the same, else False"""
        if not isinstance(other, PokemonMove):
            return False
        
        return self.name == other.name and self.energy == other.energy and self.damage == other.damage and self.effect == other.effect 