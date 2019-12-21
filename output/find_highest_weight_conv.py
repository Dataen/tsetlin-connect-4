import numpy as np

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
    filename = "conv_class_1_split_"+str(j+1)+".txt"
    file = open(filename).read()
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
            pos_plain_txt = lines[i+1]
            pos_neg_txt = lines[i+2]
            pos_plain = [[pos_plain_txt[13], pos_plain_txt[14]], [pos_plain_txt[18],pos_plain_txt[19],pos_plain_txt[20]]]
            pos_neg =[[pos_neg_txt[13], pos_neg_txt[14]], [pos_neg_txt[18],pos_neg_txt[19],pos_neg_txt[20]]]
            for k in range(4):
                state = lines[i+k+3]
                state = state.split(" ")
                clause_state.append(state)
            weights.append([weight, clauseTxt[0], filename, pos_plain, pos_neg, clause_state])
        n = n + 1
        if n==8:
            n = 0

hh=0

makeData()
weights.sort()
weights.reverse()
weights = weights[hh:hh+10]

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

def find_pos(pos):
    ip = []
    for p in pos:
        ip.append(int(p))
    if (len(ip)==2):
        #print(ip)
        if ip[0]==0 and ip[1]==0:
            return 0
        elif ip[0]==1:
            return 1
        elif ip[1]==1:
            return 2
    else:
        if ip[0]==0 and ip[1]==0 and ip[2]==0:
            return 0
        elif ip[2]==1:
            return 3
        elif ip[1]==1:
            return 2
        elif ip[0]==1:
            return 1
    return None

def does_work(x_start, x_end, y_start, y_end, data, list):
    for myx in range(x_start, x_end+1):
            for myy in range(y_start, y_end+1):
                if fits(data[myx][myy:myy+4], list[0]):
                    if fits(data[myx+1][myy:myy+4], list[1]):
                        if fits(data[myx+2][myy:myy+4], list[2]):
                            if fits(data[myx+3][myy:myy+4], list[3]):
                                return True
    return False



#Run through dataset and all clauses to test their patterns
for clause in weights:
    hh = hh + 1
    win = 0
    loss = 0
    print(hh,clause[:-1])
    rev = clause[-1]
    clause[-1].reverse()
    list = []
    doneW = False
    doneL = False
    n = 0
    m = 0

    pos_plain_x = clause[3][1]
    pos_plain_y = clause[3][0]
    pos_negat_x = clause[4][1]
    pos_negat_y = clause[4][0]

    x_start = find_pos(pos_plain_x)
    x_end = find_pos(pos_negat_x)
    y_start = find_pos(pos_plain_y)
    y_end = find_pos(pos_negat_y)

    if x_start >= x_end:
        continue
    if y_start >= y_end:
        continue

    #print("X:", x_start, x_end)
    #print("Y:", y_start, y_end)

    for a,b,c,d in zip(*rev):
        list.append([a,b,c,d])


    #list = clause[-1]
    for line in new_lines:
        data = line.split(",")[:-1]
        data = np.reshape(data, (-1, 6))

        #
        #data = np.rot90(data)

        if does_work(x_start, x_end, y_start, y_end, data, list):
            data_label = line.split(",")[-1]
            if data_label == "win":
                win = win + 1
                m = m + 1
                if not doneW and m==500:
                    print("Example Win Match")
                    doneW = True
                    data = np.rot90(data)
                    data = data.tolist()
                    for d in data:
                        print(d[0], d[1], d[2], d[3], d[4], d[5], d[6])
            else:
                loss = loss + 1
                n = n + 1
                if not doneL and n==1:
                    print("Example Loss Match")
                    doneL = True
                    data = np.rot90(data)
                    data = data.tolist()
                    for d in data:
                        print(d[0], d[1], d[2], d[3], d[4], d[5], d[6])

    print("Wins: ",  win, " Losses: ", loss, " Total: ", win+loss)

    results.append([clause[:-1], win, loss])

