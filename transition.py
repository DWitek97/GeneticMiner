class Transition:
    def __init__(self, name, out_arcs, in_arcs):
        """
        Transition vertex in the petri net.
        :name: Name of the transition.
        :out_arcs: Collection of ingoing arcs, to the transition vertex.
        :in_arcs: Collection of outgoing arcs, to the transition vertex.
        """
        self.name = name
        self.out_arcs = out_arcs
        self.in_arcs = in_arcs
        
    def fire(self):
        """
        Fire!
        """  
        outNotBlocked = all(arc.non_blocking() for arc in self.out_arcs)
        inNotBlocked = all(arc.non_blocking() for arc in self.in_arcs)
        # Note: This would have to be checked differently for variants of
        # petri  nets that take more than once from a place, per transition.
        notBlocked = outNotBlocked and inNotBlocked
        
        for arc in self.out_arcs:
            arc.trigger()
        for arc in self.in_arcs:
            arc.trigger()
        return notBlocked # return if fired, just for the sake of debuging