import  time 
import  RPi.GPIO as GPIO
from 	sys 	 import argv
from 	math 	 import *

SENSOR_HIT 	= False
LED_ON 		= True

class TargetIo:
	def __init__(self, tickTime = 10, pollTime = .0001, targetHitTime = 2):
		self.tickTime 		= tickTime
		self.pollTime 		= pollTime
		self.targetHitLength 	= targetHitTime 
		self.lastHit  		= {}

	def setLedState(self, target):

		pin 	 = target.led
		wasHit   = target.wasHit()
	
		if (wasHit):
			GPIO.output(pin, not wasHit)
		elif(target.isMoving):
			# handle if the target is moving
			GPIO.output(pin, target.movingState)
		else:
			GPIO.output(pin, not wasHit)

	def reset(self, targets):
		for target in targets:
			target.hit = False
			setLedState(target)
		
	def targetHit(self, target): 	
		'''
		Increases the hit count of the target
		'''
		isValidHit = False
		firstHit   = self.lastHit.has_key(target.name)
		if (not firstHit):
			isValidHit = True
			self.lastHit[target.name] = time.time()
		else:
			# here we check to see if the target was hit 
			# but that the target we hit, is in the process
			# of being hit, and the polling loop is faster
			# than the response of the DIO sensor or someone
			# is pressing the target 
			currTime  = time.time()
			lastTime  = self.lastHit[target.name]
			self.lastHit[target.name] = currTime
			if (currTime - lastTime > self.targetHitLength):
				isValidHit = True
				 
		if (isValidHit):
			target.hit = target.hit + 1
		self.setLedState(target)

		return isValidHit

	def printTarget(self, target):
		print "\tTarget: %d" %(target.id)
		print "\t\tName: %s" %(target.name)
		print "\t\t LED:    %d" % (target.led)
		print "\t\t Sensor: %d" % (target.input)
		print "\t\t Status: %d" % (target.status)
		print "\t\t Moving: %s" % (str(target.isMoving))

	def configPins(self, targets):
		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BOARD)
		for target in targets:
			self.printTarget(target)
			GPIO.setup(target.input, GPIO.IN)
			GPIO.setup(target.led,   GPIO.OUT)
			self.setLedState(target)

	def notifyGameWithTargets(self, targets, notifier = None):
		'''
		This will be used later to tell the game client that 
		a target was hit 
		'''
		for target in targets:
			print "\t",target
		print 

		if (notifier is not None):
			notifier.__call__(targets)

	def checkForHits(self, targets):
		hits 	= {}
		for target in targets:
			pin    = target.input
			isHigh = GPIO.input(pin)
			if (isHigh == SENSOR_HIT):
				if (target.isMoving and not target.movingState):
					continue

				wasNewHit = self.targetHit(target)
				# this part just makes sure we track all
				# hit targets
				if (wasNewHit):
					hits[target.id] = target
					print "\t","Target hit"
		return hits

	def updateMovingTargets(self, targets):
		'''
		Updates the moving targets
		'''
		for target in targets:
			target.updateMovingTime()
			self.setLedState(target)

	def run(self, game, notifier = None):
		self.configPins(game.targets)
		self.lastHit = {}

	  	# get the pertinent data
	  	targets   	= game.targets
  		name      	= game.name   
		t  	  	= self.pollTime
		targetsHit   	= 0
		totalTargets 	= len(targets)

		for target in targets:
			target.reset()
	
		hits 		= {}  
		totalTime 	= game.totalTime
		prevElapsed 	= 0
		elapsed		= 0 
		startTime  	= time.time()
	
		while targetsHit < totalTargets and totalTime > elapsed:
		     	time.sleep(t)
			# check for hit targets
			newHits = self.checkForHits(targets)
			# then make the ones that are 'moving' move by 
			# blinking
			self.updateMovingTargets(targets)

			if (len(newHits) > 0):
				self.notifyGameWithTargets(targets, notifier = notifier)

			# determine how many were hit...could be re-written
			targetsHit = 0
			for target in targets:
				if (target.hit > 0):
					targetsHit = targetsHit + 1

			# then update the elapsed time			
			tempTime	= time.time()
			elapsed		= tempTime - startTime
			if (elapsed - prevElapsed > self.tickTime):
				print "Time Spent %.2f - Targets Destroyed - %d" % (elapsed, targetsHit)
				prevElapsed = elapsed

		endTime  		= time.time()
		game.elapsedTime 	= endTime - startTime
  
		if (totalTime > elapsed):
			print "All targets hit!"
		else:
			print "Timeout! "




