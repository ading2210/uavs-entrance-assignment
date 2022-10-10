import math

#==== various utilities and classes used in the pathfinding function ==== 
#the intersection algorithm is an implementation of the algorithm shown here:
#https://www.geeksforgeeks.org/check-if-two-given-line-segments-intersect/

#class for a point
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __repr__(self):
        return "Point"+str([self.x, self.y])
        
#class for a line segment
class Segment:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
    def __repr__(self):
        return "Segment"+str({"p1": self.p1, "p2": self.p2})

#check the orientation of a point relative to a line segment
#-1 = right, 1 = left, 0 = colinear
def orientation(segment, point):
   a = ((segment.p2.x - segment.p1.x) * (point.y - segment.p1.y) - 
        (point.x - segment.p1.x) * (segment.p2.y - segment.p1.y))
   return min(1, (max(a, -1)))

#get distance between two points
def distance(p1, p2):
    return math.sqrt((p1.x-p2.x)**2 + (p1.y-p2.y)**2)

#check if a point is on a line segment
def onSegment(segment, point):
    return math.isclose(distance(segment.p1, point) + distance(segment.p2, point), 
                        distance(segment.p1, segment.p2))

#check if two line segments are intersecting
def checkIntersect(l1, l2):
    #get orientations of each point relative to the other line segment
    o1 = orientation(l1, l2.p1)
    o2 = orientation(l1, l2.p2)
    o3 = orientation(l2, l1.p1)
    o4 = orientation(l2, l1.p2)
    
    #general cases
    if (o1 != o2 and o3 != o4):
        return True
    
    #cover edge cases where some of the points are colinear
    elif (o1 == 0 and onSegment(l1, l2.p1)):
        return True
    elif (o2 == 0 and onSegment(l1, l2.p2)):
        return True
    elif (o3 == 0 and onSegment(l2, l1.p1)):
        return True
    elif (o4 == 0 and onSegment(l2, l1.p2)):
        return True
    return False

#produce a hash of a point through a bitwise shift
#negative numbers don't work but it doesn't matter 
#since coords will never be negative
def hashPoint(point):
    yBitLength = int(point.y).bit_length()
    return (int(point.x) << yBitLength) | int(point.y)