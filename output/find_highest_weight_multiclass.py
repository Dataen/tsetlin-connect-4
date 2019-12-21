import numpy as np
import random

weights = []
lowest = 1
new_lines = []

#Grab dataset
def makeData():
    print("Making dataset")
    file = open("connect-4.data").read()
    lines = file.split("\n")
    for line in lines:
        if line.split(",")[-1] == "draw":
            continue
        new_lines.append(line)

#Find all clauses with their weights from all clauses in the 10 splits
for j in range(10):
    filename = "multiclass_class_1_split_"+str(j+1)+".txt"
    file = open(filename, 'r', encoding='utf-8').read()
    lines = file.split("\n")
    n = 0
    for i in range(len(lines)-1):
        if n==0:
            clauseTxt = lines[i]
            clauseTxt = clauseTxt.split(":")
            weight = float(clauseTxt[1])
            if weight > lowest:
                lowest = weight

            clause_state =  []
            for k in range(6):
                state = lines[i+k+1]
                state = state.split(" ")[1:]
                clause_state.append(state)
            weights.append([weight,clauseTxt[0], filename, clause_state])

        n = n + 1
        if n==9:
            n = 0

makeData()
weights.sort()
weights.reverse()
#weights = weights[:10]

results = []

def fits(dataset, clause):
    works = True
    for i in range(len(clause)):
        item = clause[i]
        if item == "*":
            continue
        elif item == "b":
            if dataset[i] != "b":
                return False
        elif item == "x":
            if dataset[i] != "x":
                return False
        elif item == "o":
            if dataset[i] != "o":
                return False
        elif item == "x̄":
            if dataset[i] == "x":
                return False
        elif item == "ō":
            if dataset[i] == "o":
                return False
    return True

llu = 0

for clause in weights:
    llu = llu + 1
    win = 0
    loss = 0
    #print(clause[:-1])
    rev = clause[-1]
    clause[-1].reverse()
    list = []
    doneW = False
    doneL = False
    n = 0
    m = 0
    for a,b,c,d,e,f in zip(*rev):
        list.append([a,b,c,d,e,f])
    for line in new_lines:
        data = line.split(",")[:-1]
        data = np.reshape(data, (-1, 6))
        if fits(data[0], list[0]):
            if fits(data[1], list[1]):
                if fits(data[2], list[2]):
                    if fits(data[3], list[3]):
                        if fits(data[4], list[4]):
                            if fits(data[5], list[5]):
                                if fits(data[6], list[6]):
                                    data_label = line.split(",")[-1]
                                    if data_label == "win":
                                        win = win + 1
                                        m = m
                                        if not doneW and m==50:
                                            print("Win")
                                            doneW = True
                                            data = np.rot90(data)
                                            data = data.tolist()
                                            for d in data:
                                                print(d[0], d[1], d[2], d[3], d[4], d[5], d[6])
                                    else:
                                        loss = loss + 1
                                        n = n
                                        if not doneL and n==50:
                                            print("Loss")
                                            doneL = True
                                            data = np.rot90(data)
                                            data = data.tolist()
                                            for d in data:
                                                print(d[0], d[1], d[2], d[3], d[4], d[5], d[6])
                                            #for a,b,c,d,e,f in zip(*data):
                                            #    print(a, b, c, d, e, f)


    print("Clause",clause[1],"Clause:",clause[0],clause[2],"Wins: ",  win, " Losses: ", loss, " Total: ", win+loss)

    results.append([clause[:-1], win, loss])


#for result in results:
#    print(result)


