class Place:
    def __init__(self, holding, name):
        """
        Place vertex in the petri net.
        :holding: Numer of token the place is initialized with.
        """
        self.name = name
        self.holding = holding