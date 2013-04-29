import os 
import json
from string  import lower
from utility import *

class GameManager:
	def __init__(self):
		self.games = {}

	def readGames(self, path, totalTime):
		'''
		Reads the game data from file
		'''
		self.games 	= {}
		dirs 		= os.listdir(path)
		for name in dirs:
			targets = createTargets(lower(os.path.join(path, name)))
			game 	= Game(targets, name, "", totalTime)
			self.games[name] = game
		return self.games
	def hasGame(self, game):
		'''
		Determines if the game manager has a reference to a game
		'''
		return self.games.has_key(game)	
	def getGame(self, game):
		if (self.hasGame(game)):
			return self.games[game]
		return None
	def __str__(self):
		x = repr(self.games.keys())
		x = x.replace("'", '"')
		return '{"games": %s}' % (x)
				
class Game:
	def __init__(self, targets, name, groupName, t):
		self.name      	 = name
		self.targets   	 = targets
		self.groupName 	 = groupName
		self.totalTime   = t 
		self.totalHits 	 = 0
		self.elapsedTime = 0
	
	def getTargetsJson(self):
		return '{"targets": %s}' % (str(self.targets))
	
