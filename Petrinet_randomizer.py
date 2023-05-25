import random
"""
Modeling approach:
  * define Petri nets in terms of their transactions
  * define transactions in terms of the actions of their arcs
  * define arcs in terms with their action on their in- or outgoing place
  * define places as basic containers
  
Run with python 2 or 3, for the example coded up in in __main__, via
  python petri_net.py --firings 10 --marking 1 2 3 2
  
References:
 * https://en.wikipedia.org/wiki/Petri_net
 * https://www.amazon.com/Understanding-Petri-Nets-Modeling-Techniques/dp/3642332773
"""

class Place:
    def __init__(self, holding, name):
        """
        Place vertex in the petri net.
        :holding: Numer of token the place is initialized with.
        """
        self.name = name
        self.holding = holding

    
class ArcBase:
    def __init__(self, place, amount=1):
        """
        Arc in the petri net. 
        :place: The one place acting as source/target of the arc as arc in the net
        :amount: The amount of token removed/added from/to the place.
        """
        self.place = place
        self.amount = amount
        

class Out(ArcBase):
    def trigger(self):
        """
        Remove token.
        """
        self.place.holding -= self.amount
        
    def non_blocking(self):
        """
        Validate action of outgoing arc is possible.
        """
        return self.place.holding >= self.amount 
        

class In(ArcBase):  
    def trigger(self):
        """
        Add tokens.
        """
        self.place.holding += self.amount

    def non_blocking(self):
        return self.place.holding == 0
            

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
        if notBlocked:
            for arc in self.out_arcs:
                arc.trigger()
            for arc in self.in_arcs:
                arc.trigger()
        return notBlocked # return if fired, just for the sake of debuging
    

class PetriNet:
    def __init__(self, transitions):
        """
        The petri net runner.
        :transitions: The transitions encoding the net.
        """
        self.transitions = transitions
    
    def run(self, firing_sequence, ps):
        """
        Run the petri net.
        Details: This is a loop over the transactions firing and then some printing.
        :firing_sequence: Sequence of transition names use for run.
        :ps: Place holdings to print during the run (debugging).
        """
        
        print("Using firing sequence:\n" + " => ".join(firing_sequence))
        print("start {}\n".format([p.holding for p in ps]))
        
        for name in firing_sequence:
            for transition in self.transitions.values():
                if name == transition.name:
                    t = transition
                    if t.fire():
                        print(name ," fired!")
                        print("  =>  {}".format([p.holding for p in ps]))
                    else:
                        print(name, " didn't fire.")
        
        print("\nfinal {}".format([p.holding for p in ps]))
            

def createTransitions(listOfTransitions, listOfPlaces):
    transitionsList = {}
    for transition in listOfTransitions:
        
        duplicateList = []
        listOfOut = []
        listOfIn = []
        alreadyExists = False
        
        amountOfOutArcs = random.randint(1,4)
        amountOfInArcs = random.randint(1,4)

        for i in range(amountOfOutArcs):
            index = random.randint(0, len(listOfPlaces) -1 )
            for outArc in duplicateList:
                if listOfPlaces[index].name == outArc.place.name:
                    alreadyExists = True
            if not alreadyExists:
                duplicateList.append(Out(listOfPlaces[index]))
                listOfOut.append(Out(listOfPlaces[index]))
            alreadyExists = False

        for i in range(amountOfInArcs):
            index = random.randint(0, len(listOfPlaces) -1 )
            for inArc in duplicateList:
                if listOfPlaces[index].name == inArc.place.name:
                    alreadyExists = True
            if not alreadyExists:
                duplicateList.append(In(listOfPlaces[index]))
                listOfIn.append(In(listOfPlaces[index]))
            alreadyExists = False

        transitionsList[transition] = Transition(transition, listOfOut, listOfIn)

    return transitionsList

def createPlaces(amountOfPlaces):
    listOfPlaces = [Place(1,"1")]
    for i in range(amountOfPlaces):
        listOfPlaces.append(Place(0, i + 1))
    return listOfPlaces


def printPetriNet(petriNet):
    for transition in petriNet.transitions:
        print("Transition: ", transition)
        for outArc in petriNet.transitions[transition].out_arcs:
            print("Places going into Transition ", transition, " : ", outArc.place.name)
        for inArc in petriNet.transitions[transition].in_arcs:
            print("Places that come after Transition ", transition, " : ", inArc.place.name)

if __name__ == "__main__":    

    listOfTransitions = ["A", "B", "C", "D", "E", "F", "G", "H"]

    amountOfPlaces = len(listOfTransitions) + random.randint(0, len(listOfTransitions)/2)
    listOfPlaces = createPlaces(amountOfPlaces)
    transitions = createTransitions(listOfTransitions, listOfPlaces)

    #static for debugging
    ps = [Place(1, "1"), Place(0, "2"), Place(1, "3"), Place(0, "4")]
    ts = dict(
        t1=Transition("A", [Out(ps[0])], [In(ps[1])]), 
        t2=Transition("B", [Out(ps[2])], [In(ps[0])]),
        )


    
    firing_sequence = ["A", "B", "C", "D", "E", "F", "G", "H"] # alternative deterministic example
    firing_sequence2 = ["A", "B", "H"]
    petri_net = PetriNet(transitions)

    #printPetriNet(petri_net)
    petri_net.run(firing_sequence2, listOfPlaces)
    