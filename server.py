import json, types
from   tornado import websocket
import tornado
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import threading 
from jsonTargets 	import *
from target		import Target
from targetIo 		import *
from string  		import *
from games   		import *

# Stackoverflow.com - questions 6131915
class ServerGame(tornado.websocket.WebSocketHandler):
	def open(self):
		print "*** web socket opened ***"
		self.gameDir 	= "./games"
		self.gameQuery 	= "getgames"
		self.gameStart 	= "startgame"
		self.gameStop   = "stopgame"
		self.games 	= {}

		self.manager 	= GameManager()
		self.manager.readGames(self.gameDir, 120)
		self.gameThread	= None
		self.gameProc 	= TargetIo()
							
	def on_message(self, message):
		print "\t", "Message from client: " + message
		data 		= json.loads(lower(message))
		newGame 	= None
		messageOut 	= ""
		if (data.has_key(self.gameQuery)):
			messageOut = u"%s"%(self.manager)
			self.write_message(messageOut)
		elif (data.has_key(self.gameStart)):
			# this part starts a new game...
			gameId 	= data[self.gameStart]
			game 	= self.manager.getGame(gameId)
			
			if (game is not None):
			  	messageOut 	= self.jsonTargets(game.targets) 
				newGame 	= game
				
			else:
			  	messageOut = u'{"targets":null}' % (self.gameStart)			

			self.write_message(messageOut)
			if (newGame is not None):
				if (self.gameThread is not None):
					self.kill()
				self.spawn(newGame)

		elif (data.has_key(self.gameStop)):
			print "aborting game..."
			self.kill()
		else:
			# this part starts a 
			messageOut = u"You said this: %s" % (message)
			print "\t"*2, ">> Message Out: ", messageOut
			self.write_message(messageOut)
		
	def kill(self):
		'''
		 need to kill the running thread
		'''
		self.gameProc.abort()
		self.gameThread.join()
		self.gameThread = None

	def spawn(self, game):
		# create a new game and spawn 
		# a thread to run 

		self.gameThread = threading.Thread(target=self.gameProc.run, args=(game, self.notify))
		self.gameThread.start()
		

	def on_close(self):
		print "*** web socket closed ***"
	
	def notify(self, targets):
		messageOut = ConvertTargetsToJson(targets)
		print "\t"*2, "Notifying targets hit", messageOut
		self.write_message("%s" % (messageOut))


def startWeb(port, timeout = 120):
	application = tornado.web.Application([
		(r'/ws', ServerGame),
	])

	http_server = tornado.httpserver.HTTPServer(application)
	http_server.listen(port)
	tornado.ioloop.IOLoop.instance().start()
		

if __name__ == "__main__":
	startWeb(4500, timeout = 120)






