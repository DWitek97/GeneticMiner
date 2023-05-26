import math

class PetriNet():
    def __init__(self, transitions, places):
        """
        The petri net runner.
        :transitions: The transitions encoding the net.
        """
        self.transitions = transitions
        self.places = places
        self.accuracy = 0
    
    def run(self, firing_sequence):
        """
        Run the petri net.
        Details: This is a loop over the transactions firing and then some printing.
        :firing_sequence: Sequence of transition names use for run.
        :ps: Place holdings to print during the run (debugging).
        """
        
        print("Using firing sequence:\n" + " => ".join(firing_sequence))
        print("start {}\n".format([p.holding for p in self.places]))
        
        for name in firing_sequence:
            for transition in self.transitions.values():
                if name == transition.name:
                    t = transition
                    if t.fire():
                        print(name ," fired!")
                        print("  =>  {}".format([p.holding for p in self.places]))
                    else:
                        print(name, " didn't fire.")
        
        print("\nfinal {}".format([p.holding for p in self.places]))

    def printPetrinet(self):
        for transition in self.transitions:
            print("Transition: ", transition)
            for outArc in self.transitions[transition].out_arcs:
                print("Places going into Transition ", transition, " : ", outArc.place.name)
            for inArc in self.transitions[transition].in_arcs:
                print("Places that come after Transition ", transition, " : ", inArc.place.name)

    def printProducedConsumed(self):
        for transition in self.transitions:
            print("Transition: ", transition)
            for outArc in self.transitions[transition].out_arcs:
                print("Consumed ", transition, " : ", outArc.consumed)
            for inArc in self.transitions[transition].in_arcs:
                print("Produced ", transition, " : ", inArc.produced)

    def reset(self):
        for transition in self.transitions:
            for outArc in self.transitions[transition].out_arcs:
                outArc.consumed = 0
                outArc.missing = 0
                outArc.place.holding = 0
            for inArc in self.transitions[transition].in_arcs:
                inArc.produced = 0
                inArc.place.holding = 0
        self.places[0].holding = 1

    def calculateFitness(self):
        pass

    def calcualteAccuracy(self):
        pass

    # Counts all tokens remaining in the self with absolute values. [-1, 1, 0] => 2 remaining tokens
    def getAllRemainingTokens(self):
        diff = 0
        for place in self.places:
            diff += math.abs(place.holding)
        return diff
        

    # Gets the count of all tokens, that have been consumed and produced during the run of the self
    def getConsumedAndProducedTokens(self):
        pass