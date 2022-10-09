#Amador UAVS software entrance assignment part 2
#written by Allen Ding

#read the input file
f1 = open("rotate.in", "r")
inputStr = f1.read().strip()
f1.close()

#parse the input and extract the relavent values
inputSplit = inputStr.split(" ")
hAOV = float(inputSplit[0])
vAOV = float(inputSplit[1])
outputLength = float(inputSplit[2])
targetX = float(inputSplit[3])
targetY = float(inputSplit[4])

print(hAOV, vAOV, outputLength, targetX, targetY)