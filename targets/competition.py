import RPi.GPIO as GPIO
import time 
from math import *
from target import *
from utility import *
from string  import *
from groupConfig import *

SENSOR_HIT 	= False
LED_ON 		= True

def setLedState(target):

	pin 	 = target.led
	wasHit   = target.wasHit()
	
	if (wasHit):
		GPIO.output(pin, not wasHit)
	elif(target.isMoving):
		# handle if the target is moving
		GPIO.output(pin, target.movingState)
	else:
		GPIO.output(pin, not wasHit)

def reset(targets):
	for target in targets:
		target.hit = False
		setLedState(target)
		
def targetHit(target): 	
	target.hit = target.hit + 1
	target.hitEvents.append(time.time())
	setLedState(target)

def configPins(targets):
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BOARD)
	for target in targets:
		print "\tTarget: %d" %(target.id)
		print "\t\tName: %s" %(target.name)
		print "\t\t LED:    %d" % (target.led)
		print "\t\t Sensor: %d" % (target.input)
		print "\t\t Friend: %s" % (str(target.isFriend))
		print "\t\t Moving: %s" % (str(target.isMoving))
		GPIO.setup(target.input, GPIO.IN)
		GPIO.setup(target.led,   GPIO.OUT)
		setLedState(target)
	print "\t", "-"*20,  "end config", "-"*20

def checkForHits(targets):
	hits = {}
	for target in targets:
		pin    = target.input
		isHigh = GPIO.input(pin)
		if (isHigh == SENSOR_HIT):
			targetHit(target)
			if (not hits.has_key(target.id)):
				hits[target.id] = target
	return hits

def updateMovingTargets(targets):
	'''
	Updates the moving targets
	'''
	for target in targets:
		target.updateMovingTime()
		setLedState(target)

def run(config):
  configPins(config.targets)

  # get the pertinent data
  targets   = config.targets
  name      = config.name 
  groupName = config.groupName

  t 		= .0001  # duty cycle per check
  targetsHit   	= 0
  totalTargets 	= len(targets)
  #raw_input("Press Any Key to Start %s: " % (name))

  for target in targets:
	target.reset()

  hits 		= {}  
  startTime  	= time.time()

  while targetsHit < totalTargets:
     	time.sleep(t)
	nextHits =  checkForHits(targets)
	for hit in nextHits.keys():
		if(not hits.has_key(hit)):
			hits[hit] = nextHits[hit]
	targetsHit  = len(hits.keys())	
	updateMovingTargets(targets)

  endTime  		= time.time()
  config.elapsedTime 	= endTime - startTime
  
  if (config.elapsedTime < totalTime):
	print "All targets hit"
  else:
	print "Timeout!"

def startGroup(tests, totalTime, name="dev"):
	isOk  = False
	group = GroupConfig(name)	

	for test in tests:
		targets = createTargets(test)
		# create a configuration
		config  = Config(targets, test, name, totalTime)
		run(config)

		# Make sure that way track the current run.
		group.configs.append(config)	
	return group

def isQuitCommand(command):
	x = {"q": True,
	     "quit": True}
	
	if (x.has_key(command)):
		return x[command]
	return False

def writeGroup(group):
	print "Group: %s" % (group.name)

def printTests(tests):
	testHeader = "Tests"
	print "-"*80	
	print " "*(len(testHeader) / 2),
	print testHeader
	print "-"*80
	for test in tests.keys():
		print "\t", test
	print 

if __name__ == "__main__":
	path 	  = "./games"	
	totalTime = 2 * 60

	# read in the tests
	tests    = {} 
	preTests = os.listdir(path)
	for test in preTests:
		targets = createTargets(lower(os.path.join(path, test)))
		config  = Config(targets, test, "", totalTime) 
		tests[config.name] = config

	# then run
	groups 	= []
	isQuit 	= False
	while(not isQuit):
		printTests(tests)
		time.sleep(5)
		#command = raw_input("Command: [type game name to start] ")
		command = "one"
		print command
		command = lower(command)
		isQuit  = isQuitCommand(command)
		if (not isQuit):
			if (tests.has_key(command)):
				run(tests[command])
			
	
	for group in groups:
		writeGroup(group)			
		
