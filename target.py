import time 
import json	

class Target:
	def __init__(self, name, id, ledPin, inputPin, status, isMoving, duty, spawnRate, points, x, y, z):
		self.name          = name	
		self.id	           = id
		self.hit           = 0
		self.led           = ledPin
		self.input         = inputPin
		self.status        = status
		self.isMoving 	   = isMoving
		self.dutyCycle 	   = duty
		self.startTime	   = 0
		self.movingState   = False
		self.spawnRate     = spawnRate
		self.points  	   = points
		self.x 		   = x
		self.y 	  	   = y
		self.z 		   = z
		self.__lastHit     = None
	def setHit(self, timeValue):
		self.__lastHit = timeValue
	def getLastHit(self):
		return self.__lastHit
	def wasHit(self):
		return self.hit > 0
	def reset(self):
		self.__lastHit = None
		self.hit = 0
	def isSpawning(self):
		if (self.__lastHit is None):
			return False
		
		t    = time.time()
		diff = t - self.__lastHit
		return (diff < self.spawnRate)
		
	def updateMovingTime(self):
		if (not self.isMoving):
			return
		
		if (self.isSpawning()):
			self.startTime = time.time()
			return
	
		if (self.startTime == None):
			self.startTime = time.time()
		currTime = time.time()
		elapsed  = currTime - self.startTime
		if (elapsed > self.dutyCycle):
			self.startTime = currTime
			self.movingState = not self.movingState
	def __str__(self):
		return json.dumps(self.__dict__)	
