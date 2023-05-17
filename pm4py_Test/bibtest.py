from pm4py.objects.petri_net import PetriNet, Marking, importer, replay
from pm4py.algo.conformance.tokenreplay import factory as token_replay_factory
import pandas
import pm4py

# Ein neues Petri-Netz erstellen
net = PetriNet("Mein Petri-Netz")

# Stellen (Places) hinzufügen
place1 = net.add_place("Place 1")
place2 = net.add_place("Place 2")
place3 = net.add_place("Place 3")
place4 = net.add_place("Place 4")
place5 = net.add_place("Place 5")

# Transitionen hinzufügen
A = net.add_transition("A")
B = net.add_transition("B")
C = net.add_transition("C")
D = net.add_transition("D")
# Kanten hinzufügen
net.add_arc(place1, A)
net.add_arc(A, place2)
net.add_arc(A, place3)
net.add_arc(place2, B)
net.add_arc(place3, C)
net.add_arc(B, place4)
net.add_arc(C, place4)
net.add_arc(place4, D)
net.add_arc(D, place5)
# Initiale und finale Markierungen festlegen
initial_marking = Marking()
initial_marking[place1] = 1  # 1 Token in Place 1 zu Beginn

final_marking = Marking()
final_marking[place5] = 1  # 1 Token in Place 1 am Ende

log = pm4py.read_xes('running-example-exported.xes')

# Tokenreplay durchführen
replayed_traces = token_replay_factory.apply(log, net, initial_marking, final_marking)

# Ergebnisse anzeigen
for case_index, replayed_trace in enumerate(replayed_traces):
    print(f"Replayed Trace {case_index}:")
    for step in replayed_trace:
        print(step)

# if __name__ == "__main__":
#     event_log = pm4py.format_dataframe(pandas.read_csv('running-example.csv', sep=';'), case_id='case_id',
#                                            activity_key='activity', timestamp_key='timestamp')
#     pm4py.write_xes(event_log, 'running-example-exported.xes')