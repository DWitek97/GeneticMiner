import random
import Petrinet
from transition import Transition
from place import Place
from arc import In
from arc import Out

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




def createTransitions(listOfTransitions, listOfPlaces):
    transitionsList = {}
    for transition in listOfTransitions:
        
        duplicateList = []
        listOfOut = []
        listOfIn = []

        # checks if arc already exists to avoid 1-loops since most nets 
        # dont have 1-loops anyways it also improves the accuarcy of the nets.
        # Can be removed if wanted, tokenreplay also works with 1-loops.
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
    pnet = Petrinet.PetriNet(transitions, listOfPlaces)

    #printPetriNet(p_net)
    pnet.run(firing_sequence)
    pnet.reset()
    pnet.run(firing_sequence)

    print("Times run: ", pnet.timesRun)
    print("Accuracy: " ,pnet.calcualteAccuracy())

    generations = 1000
    population = 100
    mutateRate = 0.1
    elitismRate = 0.1

    listOfPetrinets = []

    for i in range(generations):
        for nets in range(population):
            amountOfPlaces = len(listOfTransitions) + random.randint(0, len(listOfTransitions)/2)
            listOfPlaces = createPlaces(amountOfPlaces)
            transitions = createTransitions(listOfTransitions, listOfPlaces)
            listOfPetrinets.append(Petrinet.PetriNet(transitions, listOfPlaces))
    print(len(listOfPetrinets))

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
       