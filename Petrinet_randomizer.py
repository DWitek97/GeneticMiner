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
        self.produced = 0
        self.consumed = 0
        self.missing = 0
        self.place = place
        self.amount = amount
        

class Out(ArcBase):
    def trigger(self):
        """
        Remove token.
        """
        self.place.holding -= self.amount
        self.consumed += 1

    def non_blocking(self):
        """
        Validate action of outgoing arc is possible.
        """
        if self.place.holding >= self.amount:
            return True
        else:
            self.missing +=1
            return True 
        

class In(ArcBase):  
    def trigger(self):
        """
        Add tokens.
        """
        self.place.holding += self.amount
        self.produced += 1
        
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
        self.fitness = 0
    
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

        # checks if arc already exists to avoid 1-loops since most nets dont have 1-loops anyways it also improves the accuarcy of the nets
        # Can be removed if wanted, tokenreplay also works with 1-loops
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

def printProducedConsumed(petriNet):
    for transition in petriNet.transitions:
        print("Transition: ", transition)
        for outArc in petriNet.transitions[transition].out_arcs:
            print("Consumed ", transition, " : ", outArc.consumed)
        for inArc in petriNet.transitions[transition].in_arcs:
            print("Produced ", transition, " : ", inArc.produced)

def resetPetriNet(petriNet, listOfPlaces):
    for transition in petriNet.transitions:
        for outArc in petriNet.transitions[transition].out_arcs:
            outArc.consumed = 0
            outArc.missing = 0
            outArc.place.holding = 0
        for inArc in petriNet.transitions[transition].in_arcs:
            inArc.produced = 0
            inArc.place.holding = 0
    listOfPlaces[0].holding = 1

def calculateFitness(petriNet):
    pass

# Counts all tokens remaining in the Petrinet with absolute values. [-1, 1, 0] => 2 remaining tokens
def getAllRemainingTokens(petriNet):
    pass

# Gets the count of all tokens, that have been consumed and produced during the run of the petrinet
def getConsumedAndProducedTokens(petrinet):
    pass

if __name__ == "__main__":    

    listOfTransitions = ["A", "B", "C", "D", "E", "F", "G", "H"]

    amountOfPlaces = len(listOfTransitions) + random.randint(0, len(listOfTransitions)/2)
    listOfPlaces = createPlaces(amountOfPlaces)
    transitions = createTransitions(listOfTransitions, listOfPlaces)

    #static for debugging
    ps = [Place(1, "1"), Place(0, "2"), Place(0, "3"), Place(0, "4"), Place(0,"5")]
    ts = dict(
        t1=Transition("A", [Out(ps[0])], [In(ps[1]), In(ps[2])]), 
        t2=Transition("B", [Out(ps[1]), Out(ps[2])], [In(ps[3])]),
        t3=Transition("C", [Out(ps[2])], [In(ps[3])]), 
        t4=Transition("D", [Out(ps[3])], [In(ps[4])]),
        )


    
    firing_sequence = ["A", "B", "D", "C"] # alternative deterministic example
    firing_sequence2 = ["A", "B", "H"]
    petri_net = PetriNet(ts)

    #printPetriNet(petri_net)
    petri_net.run(firing_sequence, ps)

    #printProducedConsumed(petri_net)
    resetPetriNet(petri_net, ps)
    petri_net.run(firing_sequence, ps)

    Generations = 100
    Population = 100
    mutateRate = 0.1
    elitismRate = 0.1

    Petrinets = []
    # Generation 1 läuft durch, besten 10% selektieren, Rekombination, Mutation durchführen an den besten 10% und anschließend neue random Population generieren für restliche 90%

    # logs einlesen und als variable speichern

    # LOOP für alle Petrinetze
        #   Petrinetz erstellen 
        #   Random zahlen generieren für places und transitionen
        #   Places erstellen
        #   Transitionen erstellen

        # LOOP für ein Petrinetz
            #   Traces von log durch Petrinetz laufen lassen
            #   Nach durchlauf tokens in Places zählen
            #   Produced und consumed zählen 
            #   Accuracy berechnen
            #   Petrinetz resetten (consumed, produced, remaining) für nächstes trace
            #   Pro durchlauf Tokenreplay accuracy speichern oder average berechnen?
       