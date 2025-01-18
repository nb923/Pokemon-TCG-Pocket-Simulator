class PokemonCard:
    def __init__(self):
        self.id = None
        self.name = None
        self.stage = None
        self.evolves_from = None
        self.health = None
        self.type = None
        self.modifier = None
        self.weakness = []
        self.retreat_cost = []
        self.abilities = []
        self.moves = []

        self.states = []
        self.evo_ready = None