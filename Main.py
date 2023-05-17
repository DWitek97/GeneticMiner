

log = [['A', 'B', 'H'],['A','D','E','F','G','H'],['A','D','F','E','G','H']['A','C','H']]

def main():
    print("hi")

def parseLogs():
    pass

def readLog():
    pass

if __name__=="__main__":
    main()


class Place():
    def __init__(self, name, startingAmount = 1):
        self.startingAmount = startingAmount

class Transition():
    def __init__(self, name, edgeIn, edgeOut):
        self.name = name

class edgeIn():
    def __init__(self, place, transition):
        self.outOf = place
        self.into = transition

class edgeOut():
    def __init__(self, place, transition):
        self.outOf = place
        self.into = transition
    
    def trigger():
        pass