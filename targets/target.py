import time 
import json	

class Target:
	def __init__(self, name, id, ledPin, inputPin, isFriend, isMoving, duty):
		self.name     = name	
		self.id	      = id
		self.hit      = 0
		self.led      = ledPin
		self.input    = inputPin
		self.isFriend   = isFriend

		self.isMoving 	   = isMoving
		self.dutyCycle 	   = duty
		self.startTime 	   = None
		self.movingState   = False
		self.hitEvents 	   = []
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
	def toJson(self):
		status 	= 1
		if (self.isFriend):
			status = 0	
		d = "{'id':%d, 'hits':%d, 'status':%d}" % (int(self.id), self.hit, status)
		return d