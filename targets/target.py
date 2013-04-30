import time 
import json	

class Target:
	def __init__(self, name, id, ledPin, inputPin, status, isMoving, duty):
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
	def wasHit(self):
		return self.hit > 0
	def reset(self):
		self.hit = 0
	def updateMovingTime(self):
		if (not self.isMoving):
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
