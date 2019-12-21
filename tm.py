from pyTsetlinMachineParallel.tm import MultiClassTsetlinMachine
from pyTsetlinMachineParallel.tm import MultiClassConvolutionalTsetlinMachine2D
from sklearn.model_selection import StratifiedKFold
import numpy as np
from time import time
import random
import tmc


#############
#HYPERPARAMETERS
#############

#1500, 80, 15, weighted: True
#10000, 80, 27, weighted: False

#TsetlinMachine Hyperparameters
MULTICLASS = True
CLAUSES = 1500
T_VALUE = 80
S_VALUE = 15
PATCH_SIZE = (4,4) # (x, y)
epochs = 30
weightedClauses = True
if weightedClauses:
    T_VALUE = T_VALUE*100
#Use previously fitted state
useLoadedState = False
#Remake dataset
makeDataset = True
#Include draw in the dataset
include_draw = False
#K-fold
subsamples = 10

print("#############")
if MULTICLASS:
    print("MULTICLASS TM")
else:
    print("MULTICLASS CONV2D TM")
    print("Patch", PATCH_SIZE)
print("Make dataset", makeDataset)
if makeDataset:
    print("Draw", include_draw)
print("Clauses", CLAUSES, "T-value", T_VALUE, "S-value", S_VALUE)
print("Weighted Clauses", weightedClauses)
print("Epochs", epochs)
print("Use saved state", useLoadedState)
print("#############")

def makeData():
    print("Making dataset")
    file = open("connect-4.data").read()
    lines = file.split("\n")
    newLines = []
    i=0
    for line in lines:
        i += 1
        positions = line.split(",")
        #Skipping draw positions
        if positions[-1] == "draw":
            if not include_draw: continue
        plrX = [0]*42
        plrO = [0]*42
        isWinForX = 0
        for j in range(len(positions)):
            pos = positions[j]
            if pos == "x":
                plrX[j] = 1
            elif pos == "o":
                plrO[j] = 1
            elif pos == "win":
                isWinForX = 1
            elif pos == "loss":
                isWinForX = 0
            elif pos == "draw":
                isWinForX = 2
        
        #Dataset is rotated, so rotate back!
        
        #First reshape to 2D
        plrX = np.reshape(plrX, (-1, 6))
        plrO = np.reshape(plrO, (-1, 6))
        
        #Rotate dataset 90 degrees
        plrX = np.flipud(np.rot90(plrX))
        plrO = np.flipud(np.rot90(plrO))
            
        #Flatten list
        plrX = plrX.flatten()
        plrO = plrO.flatten()
            
        #Done with numpy
        plrX = plrX.tolist()
        plrO = plrO.tolist()
        
        newLine = plrX + plrO + [isWinForX]
        newLines.append(newLine)

    #K-fold cross validation
    random.shuffle(newLines)
    X = []
    Y = []
    for line in newLines:
        X.append(line[0:-1])
        Y.append(line[-1])
    
    kf = StratifiedKFold(n_splits=subsamples)
    print("Done")
    return np.array(X), np.array(Y), kf


def fit_tm(tm, X_train, Y_train, X_test, Y_test, resultFile, printLines):
    print("\nAccuracy over "+str(epochs)+" epochs:\n")
    for i in range(epochs):
        start = time()
        tm.fit(X_train, Y_train, epochs=1, incremental=True)
        stop = time()
        result = 100*(tm.predict(X_test) == Y_test).mean()
        resultText = ("Epoch#%d Accuracy: %.2f%% (%.2fs)" % (i+1, result, stop-start))
        resultFile.write(resultText + "\n")
        if printLines: print(resultText)
    return float(result)


#######
#RUN
#######

def run():
    
    if MULTICLASS:
        #File for save accuracy result in each epoch
        resultFile = open("multiclass_results.txt","w+")
        #File for saving TsetlinMachine state after training
        stateFile = open("multiclass_state.txt","w+")
    else:
        resultFile = open("conv_results.txt","w+")
        stateFile = open("conv_state.txt","w+")
    
    startTime = time()
    X, Y, kf = makeData()
    i=0
    totalresults = []
    #Run through each fold in k-fold
    for train_index, test_index in kf.split(X,Y):
        i = i +1
        print("\nSPLIT "+str(i) + "/" + str(subsamples))
        resultFile.write("SPLIT "+str(i)+"\n")
        X_train, X_test = X[train_index], X[test_index]
        Y_train, Y_test = Y[train_index], Y[test_index]
        
        if MULTICLASS:
            tm = MultiClassTsetlinMachine(CLAUSES, T_VALUE, S_VALUE, weighted_clauses=weightedClauses, boost_true_positive_feedback=0)
        else:
            tm = MultiClassConvolutionalTsetlinMachine2D(CLAUSES, T_VALUE, S_VALUE, PATCH_SIZE, weighted_clauses=weightedClauses, boost_true_positive_feedback=0)
            # X.shape[0] = length of dataset, shape_x = length of x-axis, shape_y = length of y-axis, shape_z = length of z-axis(if 3D)
            shape_x = 7
            shape_y = 6
            shape_z = 2
            X_train = X_train.reshape(X_train.shape[0], shape_x, shape_y, shape_z)
            X_test = X_test.reshape(X_test.shape[0], shape_x, shape_y, shape_z)
            
        result = fit_tm(tm, X_train, Y_train, X_test, Y_test, resultFile, True)
        totalresults.append(result)
        
        #PRINT CLAUSES TO FILE
        
        #split, tm, class, from, to, multiclass
        tmc.printClauses(i, tm, 0, 0, CLAUSES, MULTICLASS)
        tmc.printClauses(i, tm, 1, 0, CLAUSES, MULTICLASS)
        
        
    avg = np.mean(totalresults)
    resultFile.write("Average over "+str(subsamples)+"-fold crossover: " + str(avg)+"\n")
    endTime = time()
    resultFile.write("Total time: %.2fmin (%.2fs)" % ((endTime-startTime)/60.0, endTime-startTime))
    resultFile.close()
    
run()

print("\n FINISHED.")