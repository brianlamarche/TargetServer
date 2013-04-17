import time 

class Target:
	def __init__(self, name, id, ledPin, inputPin, isFriend, isMoving, duty):
		self.name     = name	
		self.id	      = id
		self.hit      = 0
		self.led      = ledPin
		self.input    = inputPin
		self.isFriend = isFriend

		self.isMoving 	   = isMoving
		self.dutyCycle 	   = duty
		self.startTime 	   = None
		self.movingState   = False
		self.hitEvents 	   = []
	def isHit(self):
		return self.hit
	def wasHit(self):
		self.hit = True
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
