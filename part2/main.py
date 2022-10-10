#Amador UAVS software entrance assignment part 2
#written by Allen Ding

#==== imports ====

import math
from math import radians, degrees

#==== read and parse the input ====

#read the input file
f1 = open("rotate.in", "r")
inputStr = f1.read().strip()
f1.close()

#parse the input and extract the relavent values
inputSplit = inputStr.split(" ")
hAOV = float(inputSplit[0]) #horizontal angle of view
vAOV = float(inputSplit[1]) #vertical angle of view
outputLength = float(inputSplit[2]) #desired length of image feed
targetX = float(inputSplit[3]) #x position of the target
targetY = float(inputSplit[4]) #y position of the target

#==== perform the actual calculations ====
#explanations for how each formula was derived is included in the attached images
#diagram for the altitude and width calculations is located at images/aov.png
#diagram for the roll and pitch calculations at images/roll_and_pitch.png

#get the altitude that the drone should be at
#explanation at images/altitude.png
altitude = (outputLength/2) / math.tan(radians(vAOV/2))

#get the width of the image feed after altitude adjustment
#explanation at images/width.png
outputWidth = 2 * (altitude * math.tan(radians(hAOV/2)))

#get the desired roll so that the camera is looking at (0, y)
#it's important to flip the sign of the output since a positive roll
#causes the camera to face a negative y value
#explanation at images/roll.png
roll = -degrees(math.atan(targetY/altitude))

#get the desired pitch value so that the camera is looking at (x, 0)
#explanation at images/pitch.png
pitch = degrees(math.atan(targetX/altitude))

#==== write the output values ====
#round and convert the calculated values into a single string
outputString = "{A} {W} {R} {P}".format(
    A = round(altitude, 1),
    W = round(outputWidth, 1),
    R = round(roll, 1),
    P = round(pitch, 1)
)

#write the outputted string to a file
f2 = open("rotate.out", "w")
f2.write(outputString)
f2.close()