import random
from logReader import logreader
from Petrinet import PetriNet
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


class geneticMiner():

    def __init__(self):
        self.allActivities = None
        self.generations = 1
        self.populationSize = 2
        self.mutateRate = 0.1
        self.elitismRate = 0.1
        self.listOfPetrinets = []

    def createTransitions(self, listOfTransitions, listOfPlaces):
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

    def createPlaces(self, amountOfPlaces):
        listOfPlaces = [Place(1,1)]
        for i in range(amountOfPlaces):
            if i > 0:
                listOfPlaces.append(Place(0, i + 1))
        return listOfPlaces

    def crossCombine(self, petriNet1, petriNet2):
        if len(petriNet1.places) < len(petriNet2.places):
            places = self.createPlaces(len(petriNet2.places))
        else:
            places = self.createPlaces(len(petriNet1.places))
        listOfIn = []
        listOfOut = []
        transitionList = {}
        complete = False
        while not complete:
            i = random.randint(0, len(self.allActivities) - 1)
            if i % 2 == 0:
                Tkey = list(petriNet1.transitions)[i]
                if Tkey not in transitionList:
                    for outArc in petriNet1.transitions[Tkey].out_arcs:

                        listOfOut.append(Out(places[int(outArc.place.name) - 1]))
                    for inArc in petriNet1.transitions[Tkey].in_arcs:
                        listOfIn.append(In(places[int(inArc.place.name) - 1]))
                    transitionList[Tkey] = (Transition(Tkey, listOfOut, listOfIn))
                else:
                    pass
            else:
                Tkey = list(petriNet2.transitions)[i]
                if Tkey not in transitionList:
                    for outArc in petriNet2.transitions[Tkey].out_arcs:
                        listOfOut.append(Out(places[int(outArc.place.name) - 1]))
                    for inArc in petriNet2.transitions[Tkey].in_arcs:
                        listOfIn.append(In(places[int(inArc.place.name) - 1]))
                    transitionList[Tkey] = (Transition(Tkey, listOfOut, listOfIn))
                else:
                    pass
            complete = True
            for char in self.allActivities:
                if char not in transitionList:
                    complete = False
        return PetriNet(transitionList, places)

        # for tr in petriNet1.transitions.values():
        #     for outArc in tr.out_arcs:
        #         listOfOut.append(Out(places[int(outArc.place.name)]))
        #     for inArc in tr.in_arcs:
        #         listOfIn.append(In(places[int(inArc.place.name)]))
        #     transitionList.append(Transition(tr.name, listOfOut, listOfIn))
        
    
        # neue places erstellen
        # out und in arcs anschauen und nachbauen?
        return transitionList

    def initializeStartingPopulation(self, populationSize, allActivies):
        for i in range(populationSize):
            amountOfPlaces = len(allActivies) + random.randint(0, round(len(allActivies)/2))
            listOfPlaces = self.createPlaces(amountOfPlaces)
            transitions = self.createTransitions(allActivies, listOfPlaces)
            self.listOfPetrinets.append(PetriNet(transitions, listOfPlaces))
    

    def initializeNewPopulation(self):
        pass

    def main(self):
        csv_datei = "Log.csv"
        reader = logreader()
        traces = reader.readLogs(csv_datei)
        self.allActivities = reader.getAllActivities()
        #print(self.allActivities)
        # listOfTransitions = ["A", "B", "C", "D", "E", "F", "G", "H"]

        amountOfPlaces = len(self.allActivities) + random.randint(0, round(len(self.allActivities)/2))
        listOfPlaces = self.createPlaces(amountOfPlaces)
        transitions = self.createTransitions(self.allActivities, listOfPlaces)

        self.initializeStartingPopulation(self.populationSize, self.allActivities)

        # run tokenreplay of all traces for every net
        for i in range(self.generations):
            for petriNet in self.listOfPetrinets:
                for trace in traces:
                    petriNet.run(trace)
                    petriNet.printPetrinet()
                    #petriNet.mutate()
                    petriNet.resetTokens()
                net = self.crossCombine(self.listOfPetrinets[0], self.listOfPetrinets[1])
            #net.printPetrinet()
        for net in self.listOfPetrinets:
            net.calculateFitness()
            if net.fitness > 0.01:
                print("{:.2f}".format(net.fitness))

if __name__ == "__main__":    
    miner = geneticMiner()
    miner.main()
    
    


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

   #################### static for debugging ###########################################

    # ps = [Place(1, "1"), Place(0, "2"), Place(0, "3"), Place(0, "4"), Place(0,"5")]
    # ts = dict(
    #     t1=Transition("A", [Out(ps[0])], [In(ps[1]), In(ps[2])]), 
    #     t2=Transition("B", [Out(ps[1]), Out(ps[2])], [In(ps[3])]),
    #     t3=Transition("C", [Out(ps[2])], [In(ps[3])]), 
    #     t4=Transition("D", [Out(ps[3])], [In(ps[4])]),
    #     )

    # firing_sequence = ["A", "B", "D", "C"] # alternative deterministic example
    # pnet = PetriNet(ts, ps)
    # pnet.run(firing_sequence)
    # pnet.resetTokens()
    # pnet.run(firing_sequence)
    # print("Times run: ", pnet.timesRun)
    # print("Accuracy: " ,pnet.accuracy)

    #################### static for debugging ###########################################