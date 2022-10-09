import utils
from utils import Point, Segment

#class for polygons
class Polygon:
    def __init__(self, points):
        self.points = points
        
    def __repr__(self):
        return str({"points": self.points})
    
    #check if a line segment collides with the polygon
    def checkCollision(self, segment):
        for i in range(0, len(self.points)):
            side = Segment(self.points[i-1], self.points[i])
            if (utils.checkIntersect(segment, side)):
                return True
        return False
    
#open the input file
f1 = open("navigate.in", "r")
inputString = f1.read().strip()
f1.close()

#parse the input
lines = inputString.split("\n")
argsList = lines[0].split(" ")
sizeX = int(argsList[0])
sizeY = int(argsList[1])
waypointCount = int(argsList[2])
polygonCount = int(argsList[3])

#parse list of waypoints
waypoints = []
for i in range(1, waypointCount+1):
    lineSplit = lines[i].split(" ")
    x = int(lineSplit[0])
    y = int(lineSplit[1])
    waypoints.append(Point(x, y))
    
#parse list of polygons
polygons = []
index = 1+waypointCount
for i in range(0, polygonCount):
    sides = int(lines[index])
    polygons.append(Polygon([]))
    index += 1
    for j in range(index, index+sides):
        lineSplit = lines[index].split(" ")
        x = int(lineSplit[0])
        y = int(lineSplit[1])
        polygons[i].points.append(Point(x, y))
        index += 1
        
#class for each node
class Node:
    def __init__(self, point, parent):
        self.point = point
        self.parent = parent
        self.g = 0
        self.f = 0
        self.h = 0
        
    def __repr__(self):
        return "Node"+str({
            "point": self.point,
            "g": self.g,
            "f": self.f,
            "g": self.h
        })
    
    #checks if two nodes are in the same location
    def equalTo(self, node):
        if type(node) is Point:
            return (self.point.x == node.x and self.point.y == node.y)
        return (self.point.x == node.point.x and self.point.y == node.point.y)

#the actual pathfinding algorithm
#A* is a massive pain to implement
def pathfind(start, goal):
    openList = [Node(start, None)]
    closedList = []

    while len(openList) > 0:
        #get the node with the smallest f score
        smallest = None
        currentIndex = 0
        for i in range(0, len(openList)):
            node = openList[i]
            if smallest == None or node.f < smallest.f:
                smallest = node
                currentIndex = i
        current = smallest
        
        del openList[currentIndex]
        closedList.append(current)
        
        #check if the goal has already been reached
        if current.equalTo(goal):
            path = []
            while current.parent != None:
                path.insert(0, current.point)
                current = current.parent
            return path
        
        #calculate neightbors
        neighbors = []
        offsets = [
            [-1, 0],
            [-1, -1],
            [0, -1],
            [1, -1],
            [1, 0],
            [1, 1],
            [0, 1],
            [-1, 1]
        ]
        for offset in offsets:
            point = Point(current.point.x+offset[0], current.point.y+offset[1])
            if (point.x < 1 or point.y < 1 or point.x > sizeX or point.y > sizeY):
                continue
            
            #check that the point doesn't intersect a polygon
            for polygon in polygons:
                if (polygon.checkCollision(Segment(current.point, point))):
                    break
            else:
                neighbors.append(Node(point, current))
        
        #iterate through neighbors 
        for neighbor in neighbors:
            #don't append this node if it's already been checked
            for node in closedList:
                if neighbor.equalTo(node):
                    break
            else:
                neighbor.g = current.g + utils.distance(current.point, neighbor.point)
                neighbor.h = utils.distance(current.point, goal)
                neighbor.f = neighbor.g + neighbor.h
                
                #don't append this node if it's already in openList
                for node in openList:
                    if neighbor.equalTo(node) and neighbor.g >= node.g:
                        break
                else:
                    openList.append(neighbor)

#run the pathfinding algorithm on each waypoint
path = [waypoints[0]]
for i in range(1, len(waypoints)):
    path += pathfind(waypoints[i-1], waypoints[i])
    
#save the final path
f2 = open("navigate.out", "w")
outputString = ""
for point in path:
    outputString += f"{point.x} {point.y}\n"
f2.write(outputString.strip())
f2.close()
