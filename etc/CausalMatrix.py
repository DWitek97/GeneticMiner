
log = (['A', 'B', 'H'],['A','D','E','F','G','H'],['A','D','F','E','G','H'],['A','C','H'])

def main():
    pass

def readLog():
    pass

def getAllActivites(log):
    causalMatrix = [
        [],
        [],
        []
    ]
    for trace in log:
        for activity in trace:
            if activity not in causalMatrix[0]:
                causalMatrix[0].append(activity)

    causalMatrix[0].sort()

    return causalMatrix

def findAllInputs(causalMatrix, log):
    for activity in causalMatrix[0]:
        inputs = []
        for trace in log:
            if activity in trace:
                index = trace.index(activity)
                if index > 0 and trace[index - 1] not in inputs:
                    inputs.append(trace[index - 1])
        causalMatrix[1].append(inputs)

    return causalMatrix
                

def finAllOutputs(causalMatrix, log):
    for activity in causalMatrix[0]:
        outputs = []
        for trace in log:
            if activity in trace:
                index = trace.index(activity)
                try:
                    if trace[index + 1] not in outputs:
                        outputs.append(trace[index + 1])
                except:
                    pass
        causalMatrix[2].append(outputs)

    return causalMatrix
            
def checkForConcurrency():
    pass

if __name__=="__main__":
    causalMatrix = getAllActivites(log)
    causalMatrix = findAllInputs(causalMatrix, log)
    causalMatrix = finAllOutputs(causalMatrix, log)

    for activity in causalMatrix[0]:
        print("activity: ", activity,"  inputs: ", causalMatrix[1][causalMatrix[0].index(activity)], "     Outputs: ", causalMatrix[2][causalMatrix[0].index(activity)])
        
    main()

