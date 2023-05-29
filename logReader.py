import pandas as pd

class logreader():

    def __init__(self):

        self.traces = []
        self.activities = []
        self.daten = None

    def readLogs(self, path):
        self.daten = pd.read_csv(path)
        
        for index, zeile in self.daten.iterrows():
            trace = []
            for char in zeile["Activity"]:
                trace.append(char)
            self.traces.append(list(trace)) 
        return self.traces

    def getAllActivities(self):    
        for index, zeile in self.daten.iterrows():
            for char in zeile["Activity"]:
                if char not in self.activities:
                    self.activities.append(char) 
        return self.activities

