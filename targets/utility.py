import os 
from target  import *
from string  import *

def isTrue(s):
	s = strip(lower(s))
	return s in ["true"]

def createTargets(path):
	lines 	= readFile(path)
	lines 	= map(lambda x: x[:-1], lines)
	targets = []
	for line in lines[1:]:
		data = line.split(",")
		if (len(data) > 6):
			name	 = data[0]
			id 	 = atoi(data[1])
			ledPin   = atoi(data[2])
			resPin   = atoi(data[3])
			isFriend = isTrue(data[4])
			isMoving = isTrue(data[5])
			duty     = atof(data[6])
			target   = Target(name, id, ledPin, resPin, isFriend, isMoving, duty)
			targets.append(target)
	return targets
	
def readFile(path):
	f = open(path, "r")
	lines = f.readlines()
	f.close()
	return lines
