import time
from targetIo 	import *
from string  	import lower
from games   	import Game, GameManager

class LocalGame:
	'''
		Handles the local interaction with a user
	'''
	def isQuitCommand(self, command):
		x = {"q": True,
		     "quit": True}
	
		if (x.has_key(command)):
			return x[command]
		return False


	def start(self, path):
		'''
		Runs a local game
		'''
		
		totalTime = 2 * 60
	
		# read in the tests
		gameManager 	= GameManager()
		games 		= gameManager.readGames(path, totalTime) 

		# then run
		isQuit 	= False		
		proc 	= TargetIo()

		while(not isQuit):
			print "-"*60
			print gameManager
			print "-"*60
			command = raw_input("Command: [type game name to start] ")
			command = lower(command)
			isQuit  = self.isQuitCommand(command)
			if (not isQuit):
				if (gameManager.hasGame(command)):
					print 
					print " >> Starting game."
					print 
					proc.run(games[command])
					time.sleep(5)
				else:
					print 
					print ">> That game does not exist." 
					print 

if (__name__ == "__main__"):
	game = LocalGame()
	game.start("./games")
