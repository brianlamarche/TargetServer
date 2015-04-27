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
		self.dutyCycle		= 5
		self.abortGame 		= False
		self.pins 		= [11, 15, 16, 22]
		
	def setLedState(self, target):
		pin 	 = target.led	

		# if the target is spawning...then turn it off
		if (target.isSpawning()):
			GPIO.output(pin, False)
			return 
		
		# if the target is moving...make sure it's not in a moving state
		if(target.isMoving):
			GPIO.output(pin, target.movingState)
		else:
			# otherwise we know that it's not spawning, so it wasnt hit
			# and we know it's not moving
			GPIO.output(pin, True)

	def clearAll(self, pins):
		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BOARD)
		for pin in pins:
			GPIO.setup(pin,   GPIO.OUT)			
			GPIO.output(pin, False)

	def showAll(self, pins):
		for pin in pins:
			GPIO.setup(pin,   GPIO.OUT)			
			GPIO.output(pin, True)

	def reset(self, targets):
		for target in targets:
			target.hit = 0
			self.setLedState(target)
		
	def targetHit(self, target): 	
		'''
		Increases the hit count of the target
		'''
		isValidHit = False
		t 	   = time.time()
		firstHit   = target.getLastHit()  #self.lastHit.has_key(target.name)
		if (firstHit is None):
			isValidHit = True
			target.setHit(t)
			self.lastHit[target.name] = t
		else:
			# here we check to see if the target was hit 
			# is in the process
			# of being hit, and the polling loop is faster
			# than the response of the DIO sensor or someone
			# is pressing the target 
			currTime  = t
			lastTime  = firstHit # self.lastHit[target.name]
			diff   	  = currTime - lastTime
			if (diff > self.targetHitLength):	
				# first check makes sure the polling loop isnt faster 
				if (diff > target.spawnRate):
					# the second set makes sure that the 
					# target has had enough time to respawn
					#self.lastHit[target.name] = currTime
					isValidHit = True
				 	target.setHit(t)
		if (isValidHit):
			target.hit = target.hit + 1
			if (target.canChangeSides):
				h = int(target.hit / 2)
				e = math.pow(2, h)
				m = target.hit * e
				target.points = target.points * m
			else:
				target.score  = target.points * target.hit
				
		self.setLedState(target)

		return isValidHit

	def printTarget(self, target):
		print "\tTarget: %s\t\t%.2f" %(target.name, target.hit*target.points)
		print "\t\tHits: %d" %(target.hit)
		print "\t\tID: %s" %(target.id)
		print "\t\t Points:    %d" % (target.points)
		print "\t\t Spawn Rate:    %d" % (target.spawnRate)
		print "\t\t Position:  (%.2f, %.2f, %.2f)" % (target.x, target.y, target.z)
		print "\t\t LED:    %d" % (target.led)
		print "\t\t Sensor: %d" % (target.input)
		status = {0: "Foe", 1: "Friend"}[target.status] 
		print "\t\t Status: %s" % (status)
		print "\t\t Moving: %s" % (str(target.isMoving))

	def configPins(self, targets):
		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BOARD)
		for target in targets:
			self.printTarget(target)
			GPIO.setup(target.input, GPIO.IN)
			GPIO.setup(target.led,   GPIO.OUT)
			self.setLedState(target)

	def updateMovingTargets(self, targets):
		'''
		Updates the moving targets
		'''
		for target in targets:
			target.updateMovingTime()
			self.setLedState(target)

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
			else:
				self.setLedState(target)
		return hits

	def notifyGameWithTargets(self, targets, notifier = None):
		if (notifier is not None):
			notifier.__call__(targets)

	def abort(self):
		print "Aborted Game"
		self.abortGame = True

	def flair(self, game, notify):		
		self.clearAll(self.pins)
		self.abortGame = False
		N	= len(self.pins)
		print "Resting...."
		while self.abortGame == False:
			for i in range(N):
				for pin in self.pins:
					GPIO.output(pin, False)
				GPIO.output(self.pins[i], True)
				time.sleep(.1)
			for i in range(N, 0, -1):
				for pin in self.pins:
					GPIO.output(pin, False)
				GPIO.output(self.pins[i - 1], True)
				time.sleep(.1)
			time.sleep(.2)
			for pin in self.pins:
				GPIO.output(pin, False)			
			time.sleep(.5)			
		print "flair done"
		
	def run(self, game, notifier):
		self.clearAll(self.pins)
		self.configPins(game.targets)
		self.lastHit 	= {}
		self.abortGame 	= False

	  	# get the pertinent data
	  	targets   	= game.targets
  		name      	= game.name   
		t  	  	= self.pollTime
		targetsHit   	= 0
		totalTargets 	= len(targets)
		
		self.reset(targets)	
		self.lastHits = {}
		for target in targets:
			target.reset()
			self.setLedState(target)
		
		hits 		= {}  
		totalTime 	= game.totalTime
		prevElapsed 	= 0
		elapsed		= 0 
		startTime  	= time.time()

		while  totalTime > elapsed and self.abortGame == False:
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
  
	

		print 
		for t in targets:
			self.printTarget(t)




