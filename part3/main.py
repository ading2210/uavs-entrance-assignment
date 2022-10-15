#Amador UAVS software entrance assignment part 3
#written by Allen Ding

#==== input format ====
#filename: navigate.in
#example:
#10 10 4 2
#1 1
#3 7
#...
#5
#2 4
#2 5
#...

#==== output format ====
#filename: navigate.out
#example:
#1 1 
#1 2
#1 3
#...

#==== imports ====
import utils
from utils import Point, Segment
from queue import PriorityQueue

#==== define necessary classes ====

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
            "h": self.h
        })
    
    #checks if two nodes are in the same location
    def equalTo(self, node):
        if type(node) is Point:
            return (self.point.x == node.x and self.point.y == node.y)
        return (self.point.x == node.point.x and self.point.y == node.point.y)
    
#==== read and parse the input ====
    
#open the input file
f1 = open("navigate.in", "r")
inputString = f1.read().strip()
f1.close()

#parse the input
lines = inputString.split("\n")
argsList = lines[0].split(" ")
sizeX = int(argsList[0]) #size of the grid on the x axis
sizeY = int(argsList[1]) #size of the grid on the y axis
waypointCount = int(argsList[2]) #total waypoint count
polygonCount = int(argsList[3]) #total polygon count
waypoints = [] #list of waypoints to visit
polygons = [] #list of polygons to avoid

#parse list of waypoints
for i in range(1, waypointCount+1):
    lineSplit = lines[i].split(" ")
    x = int(lineSplit[0])
    y = int(lineSplit[1])
    waypoints.append(Point(x, y))

#parse list of polygons
index = 1+waypointCount #line number to read
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
    
#==== run the actual pathfinding algorithm ====
#here i'm using the A* algorithm since it's the most efficient
#and because i already have experience using it

#function that returns a path between two points as a list of Point objects
#if there is no path found then None will be returned
def pathfind(start, goal):
    openList = PriorityQueue() #a priority queue consisting of nodes to be visited
    openList.put((0, 0, Node(start, None))) #add starting point
    closedList = [] #a list containing a list of nodes already visited
    steps = 0 #steps count

    while len(openList.queue) > 0:
        #get the node with the smallest f score        
        current = openList.get()[2]
        closedList.append(current)
        
        #check if the goal has already been reached
        if current.equalTo(goal):
            #work backwards from the goal to the start
            path = []
            while current.parent != None:
                path.insert(0, current.point)
                current = current.parent
            return path
        
        #calculate neightbors
        neighbors = []
        offsets = [
            [1, 0],
            [-1, 0],
            [0, 1],
            [0, -1],
            [1, 1],
            [1, -1],
            [-1, 1],
            [-1, -1]
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
                #calculate g, h, and f values
                neighbor.g = current.g + utils.distance(current.point, neighbor.point)
                neighbor.h = utils.distance(current.point, goal)
                neighbor.f = neighbor.g + neighbor.h
                
                #don't append this node if it's already in openList
                for item in openList.queue:
                    node = item[2]
                    if neighbor.equalTo(node) and neighbor.g >= node.g:
                        break
                else:
                    #step count is used as a tiebreak in case two priorities are the same
                    steps += 1
                    openList.put((neighbor.f, steps, neighbor))

#run the pathfinding algorithm on each waypoint
path = [waypoints[0]] #the final path to be outputted
for i in range(1, len(waypoints)):
    path += pathfind(waypoints[i-1], waypoints[i])

#==== write the final path ====

#convert the path to a string
outputString = ""
for point in path:
    outputString += f"{point.x} {point.y}\n"

#write the final output to a file
f2 = open("navigate.out", "w")
f2.write(outputString.strip())
f2.close()