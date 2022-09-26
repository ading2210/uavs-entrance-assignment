#Amador UAVS software entrance assignment part 1
#written by Allen Ding
#run with "python3 main.py"
#find.in and find.out are in the same directory as main.py

#read the input file
f1 = open("find.in", "r")
inputStr = f1.read().strip()
f1.close()

#parse the input and extract the relavent values
inputSplit = inputStr.split("\n")
gridData = inputSplit[0].split(" ")
xSize = int(gridData[0])
ySize = int(gridData[1])
dx = float(gridData[2])
dy = float(gridData[3])
count = int(gridData[4])
pointsList = inputSplit[1:count+1]

#initialize output variable
output = ""

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
  finalX = round(x)
  finalY = round(y)
  output += f"{finalX} {finalY}\n"

#write to the output file
f2 = open("find.out", "w")
f2.write(output.strip())
f2.close()