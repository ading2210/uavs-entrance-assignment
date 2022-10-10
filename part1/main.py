#Amador UAVS software entrance assignment part 1
#written by Allen Ding

#==== input format ====
#filename: find.in
#example:
#8 8 0.5 0.5 3
#2.439498 1.2343
#0.2348973 4.587536
#0.75 1.25

#==== output format ====
#filename: find.out
#example:
#5 2
#0 7
#1 2

#==== read and parse the input ====

#read the input file
f1 = open("find.in", "r")
inputStr = f1.read().strip()
f1.close()

#parse the input and extract the relavent values
inputSplit = inputStr.split("\n")
gridData = inputSplit[0].split(" ")
xSize = int(gridData[0]) #size of the grid along the x axis
ySize = int(gridData[1]) #size of the grid along the y axis
dx = float(gridData[2]) #grid accuracy along the x axis
dy = float(gridData[3]) #grid accuracy along the y axis
count = int(gridData[4]) #number of points in the input
pointsList = inputSplit[1:count+1] #list of points as a string

#initialize output list
output = [] #list containing outputted points

#==== process list of points ====

#iterate through each given point
for pointStr in pointsList:
  #extract the coordinates from each point in the input file
  pointSplit = pointStr.split(" ")
  x = float(pointSplit[0])/dx
  y = float(pointSplit[1])/dy
  
  #process the coordinate to eliminate values outside the grid
  #min(...) is used so that the output is never outside of the grid
  #max(...) is used so that the output is never negative
  x = max(min(x, xSize-1), 0)
  y = max(min(y, ySize-1), 0)
  
  #force round() to round down if the coord is equally close to two grid points
  if x%1 == 0.5:
    x -= 0.01
  if y%1 == 0.5:
    y -= 0.01
  
  #round and add those results to the output
  output.append([round(x), round(y)])
  
#==== write the outputted items ====

#convert output list into a string
outputString = ""
for point in output:
  outputString += f"{point[0]} {point[1]}\n"

#write to the output file
f2 = open("find.out", "w")
f2.write(outputString.strip())
f2.close()