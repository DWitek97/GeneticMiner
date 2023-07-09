import random
import graphviz
from arc import In
from arc import Out
class PetriNet():
    def __init__(self, transitions, places):
        """
        The petri net runner.
        :transitions: The transitions encoding the net.
        """
        self.transitions = transitions
        self.places = places
        self.fitness = 0
        self.accuracy = 0.01 # average accuracy from tokenreplay, not 0 becuase algorithm would divide by 0
        self.timesRun = 0 # times tokenreplay was run to calculate average accuracy
    
    def run(self, firing_sequence):
        """
        Run the petri net.
        Details: This is a loop over the transactions firing and then some printing.
        :firing_sequence: Sequence of transition names use for run.
        :ps: Place holdings to print during the run (debugging).
        """
        self.timesRun += 1
        #print("Using firing sequence:\n" + " => ".join(firing_sequence))
        #print("start {}\n".format([p.holding for p in self.places]))
        
        for name in firing_sequence:
            for transition in self.transitions.values():
                if name == transition.name:
                    t = transition
                    if t.fire():
                        pass
                        #print(name ," fired!")
                        #print("  =>  {}".format([p.holding for p in self.places]))
                    else:
                        pass
                        #print(name, " didn't fire.")
        self.calcualteAccuracy()
        #print("\nfinal {}".format([p.holding for p in self.places]))
        

    def createGraph(self):
        graph = graphviz.Digraph("Fittest net")
        graph.attr('node', shape = 'box')
        for transition in self.transitions:
            graph.node(transition, transition)
        graph.attr('node', shape = 'circle')
        for place in self.places:
            graph.node(str(place.name), " ")
        for transition in self.transitions:
            for outArc in self.transitions[transition].out_arcs:
                graph.edge(str(outArc.place.name), transition)
            for inArc in self.transitions[transition].in_arcs:
                graph.edge(transition, str(inArc.place.name))
        graph.render(directory='nets', view=True) 

    def printPetrinet(self):
        for transition in self.transitions:
            print("Transition: ", transition)
            for outArc in self.transitions[transition].out_arcs:
                print(outArc.place.name," -> ", transition)
            print()
            for inArc in self.transitions[transition].in_arcs:
                print(transition, " -> ", inArc.place.name)
            print()

    def printProducedConsumed(self):
        for transition in self.transitions:
            print("Transition: ", transition)
            for outArc in self.transitions[transition].out_arcs:
                print("Consumed ", transition, " : ", outArc.consumed)
            for inArc in self.transitions[transition].in_arcs:
                print("Produced ", transition, " : ", inArc.produced)

    def resetTokens(self):
        for transition in self.transitions:
            for outArc in self.transitions[transition].out_arcs:
                outArc.consumed = 0
                outArc.missing = 0
                outArc.place.holding = 0
            for inArc in self.transitions[transition].in_arcs:
                inArc.produced = 0
                inArc.place.holding = 0
        self.places[0].holding = 1

    def resetAll(self):
        for transition in self.transitions:
            for outArc in self.transitions[transition].out_arcs:
                outArc.consumed = 0
                outArc.missing = 0
                outArc.place.holding = 0
            for inArc in self.transitions[transition].in_arcs:
                inArc.produced = 0
                inArc.place.holding = 0
        self.places[0].holding = 1
        self.accuracy = 0.00001
        self.fitness = 0
        self.timesRun = 1

    def calculateFitness(self):
        if self.timesRun == 0:
            self.fitness = self.accuracy / 1
        else:
            self.fitness = self.accuracy / self.timesRun 

    def calcualteAccuracy(self):
        result = 0
        correct = self.getConsumedAndProducedTokens()
        difference = self.getAllRemainingTokens()
        if correct != 0:
            result = (correct - difference) / correct
        else:
            result = 0
        self.accuracy = self.accuracy + result

    # Counts all tokens remaining in the self with absolute values. [-1, 1, 0] => 2 remaining tokens
    def getAllRemainingTokens(self):
        diff = 0
        for place in self.places:
            diff += abs(place.holding)
        if diff == 0:
            return 0
        else:
            return diff - 1 # -1 because in a perfect run the petri net will have one remaining token in the last place, meaning it is correct and should not be counted towards the remaining tokens
        

    # Gets the count of all tokens, that have been consumed and produced during the run of the self
    def getConsumedAndProducedTokens(self):
        sum = 0
        for transition in self.transitions:
            for outArc in self.transitions[transition].out_arcs:
                sum += outArc.consumed
            for inArc in self.transitions[transition].in_arcs:
                sum += inArc.produced     
        return sum
    
    def mutate(self):
        for i in range(0, random.randint(1,3)):
            n = random.randint(0,2)

            # add place
            if n == 0:
                t_index = random.randint(0, len(self.transitions) - 1)
                out_or_in = random.randint(0,1)
                if out_or_in == 0:
                    p_index = random.randint(0, len(self.places) - 1)
                    # needed because transitions is a dict, p_index is fine because places is list type
                    Tkey = list(self.transitions)[t_index]
                    self.transitions[Tkey].out_arcs.append(Out(self.places[p_index]))
                else:
                    p_index = random.randint(0, len(self.places) - 1)
                    Tkey = list(self.transitions)[t_index]
                    self.transitions[Tkey].in_arcs.append(In(self.places[p_index]))

            # delete place
            elif n == 1:
                t_index = random.randint(0, len(self.transitions) - 1)
                out_or_in = random.randint(0,1)
                if out_or_in == 0:
                    Tkey = list(self.transitions)[t_index]
                    if len(self.transitions[Tkey].out_arcs) == 0:
                        self.transitions[Tkey].out_arcs.pop()
                else:
                    Tkey = list(self.transitions)[t_index]
                    if len(self.transitions[Tkey].out_arcs) == 0:
                        self.transitions[Tkey].in_arcs.pop()