def getActionsConv(tm, tmclass, clause):    
    player_X = []
    player_O = []
    offset_plain = 0
    offsety = 6-tm.patch_dim[1]
    offsetx = 7-tm.patch_dim[0]
    #PLAIN    
    for y in range(tm.patch_dim[1]):
        for x in range(tm.patch_dim[0]):
            for z in range(2):                
                featureid = offsety+offsetx + y*tm.patch_dim[0]*2 + x*2 + z
                offset_plain = featureid+1 # pluss på 1 :) tihi
                action_plain = tm.ta_action(tmclass, clause, featureid)
                if z == 0:
                    player_X.append(action_plain)
                else:
                    player_O.append(action_plain)
   
    #NEGATED
    for y in range(tm.patch_dim[1]):
        for x in range(tm.patch_dim[0]):
            for z in range(2):
                featureid = offset_plain + offsety+offsetx + y*tm.patch_dim[0]*2 + x*2 + z
                action_negated = tm.ta_action(tmclass, clause, featureid)
                if z == 0:
                    player_X.append(action_negated)
                else:
                    player_O.append(action_negated)
    
    pos_plain = []
    
    #Posisjon
    #print("POS PLAIN")
    for i in range(offsety+offsetx):
        pos_plain.append(tm.ta_action(tmclass, clause, i))
        
    pos_neg = []
    
    #Posisjon
    #print("POS NEGATED")
    for i in range(offsety+offsetx): 
        pos_neg.append(tm.ta_action(tmclass, clause, offset_plain+i))
                 
    return player_X, player_O, pos_plain, pos_neg 

def makeCellsConv(tm, player_X, player_O):
   
    #Size of one patch
    size = tm.patch_dim[0]*tm.patch_dim[1]
    
    player_X_p = player_X[0:size] #plain
    player_X_n = player_X[size:] #negated
    player_O_p = player_O[0:size] #plain
    player_O_n = player_O[size:] #negated
    #print(player_X_p)
    #print(player_X_n)
    #print(player_O_p)
    #print(player_O_n)
    cells = []
    #Make cells
    for i in range(tm.patch_dim[1]):
        cell = []
        for j in range(tm.patch_dim[0]):
            index = i*tm.patch_dim[1]+j
            value = "*"
            
            #Both X and O in cell
            if player_X_p[index] == 1 and player_O_p[index] == 1:
                value = "M"
            #Both X and not X in cell
            elif player_X_p[index] == 1 and player_X_n[index] == 1:
                value = "U" 
            #Both O and not O in cell
            elif player_O_p[index] == 1 and player_O_n[index] == 1:
                value = "N"
            #Both not X and not O in cell
            elif player_X_n[index] == 1 and player_O_n[index] == 1:
                value = "b" 
            #X in cell 
            elif player_X_p[index] == 1:
                value = "x"
            #not X in cell
            elif player_X_n[index] == 1:
                value = "x¯"
            #O in cell
            elif player_O[index] == 1:
                value = "o"
            #not O in cell
            elif player_O[index] == 1:
                value = "o"
            cell.append(value)
        cells.append(cell)
    return cells

def printClausePatch4x4(clauseOutputFile, cells, pos_plain, pos_neg):
    cells.reverse()
    #i = 4
    clauseOutputFile.write("Pos plain: Y:"+str(pos_plain[0])+str(pos_plain[1])+" X:"+str(pos_plain[2])+str(pos_plain[3])+str(pos_plain[4])+" \n")
    clauseOutputFile.write("Pos negat: Y:"+str(pos_neg[0])+str(pos_neg[1])+" X:"+str(pos_neg[2])+str(pos_neg[3])+str(pos_neg[4])+" \n")
    for cell in cells:
        clauseOutputFile.write(str(cell[0]) +" "+ str(cell[1]) +" "+ str(cell[2]) +" "+ str(cell[3]) + "\n")
        #i -= 1
    #clauseOutputFile.write("  a b c d \n")

def printClausePatch(clauseOutputFile, cells):
    for i in range(len(cells)):
        cell = cells[i]
        clauseOutputFile.write(str(len(cells) - i))
        for j in range(len(cell)):
            num = cell[j]
            clauseOutputFile.write(' ' + num)
            if j==len(cell)-1:
                clauseOutputFile.write('\n')
    clauseOutputFile.write("  a b c d e f g \n")

def makeCells(tm, tmclass, clause):
    player_X = []
    player_O = []
    
    #Loop over all 168 TA
    
    for i in range(tm.number_of_features):      
        action_plain = tm.ta_action(tmclass, clause, i)
        action_negated = tm.ta_action(tmclass, clause, i+84)
        #player X, 0-41, 84-125
        #player O, 42-83, 126-167
        if i < 42:
            player_X.append(action_plain)
            player_X.append(action_negated)
        else:
            player_O.append(action_plain)
            player_O.append(action_negated)
    
    #print(player_X)
    #print(player_O)
    
    cells = []
    #Make cells
    for i in range(6):
        cell = []
        j = i*7*2
        while(j < (i+1)*7*2):
            value = "*"
            if player_X[j] == 1 and player_X[j+1] == 1:
                value = "M" 
            elif player_X[j] == 1:
                value = "x"
            elif player_X[j+1] == 1:
                value = "x¯"
            
            if player_O[j] == 1 and player_O[j+1] == 1:
                value = "M" 
            elif player_O[j] == 1:
                value = "o"
            elif player_O[j+1] == 1:
                value = "o"
                
            cell.append(value)
            j += 2     
        cells.append(cell)
    return cells

def printBoard(clauseOutputFile, cells):
    cells.reverse()
    i = 6
    for cell in cells:
        clauseOutputFile.write(str(i) +" "+ str(cell[0]) +" "+ str(cell[1]) +" "+ str(cell[2]) +" "+ str(cell[3]) +" "+ str(cell[4]) +" "+ str(cell[5]) +" "+ str(cell[6]) + "\n")
        i -= 1
    clauseOutputFile.write("  a b c d e f g \n")
    
def printClauses(split, tm, tmclass, from_clause, to_clause, multiclass):
    print("Printing " + str(to_clause-from_clause) + " clauses starting at index " + str(from_clause) + " from class " + str(tmclass))
    if multiclass:
        clauseOutputFile = open("output/multiclass_class_"+str(tmclass)+"_split_"+str(split)+".txt","w+")
    else:
        clauseOutputFile = open("output/conv_class_"+str(tmclass)+"_split_"+str(split)+".txt","w+")
        
    for i in range(to_clause):
        if multiclass:
            weight = tm.clause_weight(tmclass, i)
            clauseOutputFile.write("MTM CLAUSE #"+str(i)+" Weight:"+str(weight)+" \n")
            cells = makeCells(tm, tmclass, i + from_clause)
            printBoard(clauseOutputFile, cells)
        else:
            weight = tm.clause_weight(tmclass, i)
            clauseOutputFile.write("CTM CLAUSE #"+str(i)+" Weight:"+str(weight)+" \n")
            player_X, player_O, pos_plain, pos_neg = getActionsConv(tm, tmclass, i + from_clause)
            cells = makeCellsConv(tm, player_X, player_O)
            printClausePatch4x4(clauseOutputFile, cells, pos_plain, pos_neg)
        clauseOutputFile.write("----------------\n")
    
        