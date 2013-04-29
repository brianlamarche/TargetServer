import json, types
from   tornado import websocket
import tornado
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web


from target	import Target
from targetIo 	import *
from string  	import *
from games   	import *


# Stackoverflow.com - questions 6131915
class ServerGame(tornado.websocket.WebSocketHandler):
	def open(self):
		print "*** web socket opened ***"
		self.gameDir 	= "./games"
		self.gameQuery 	= "getgames"
		self.gameStart 	= "startgame"
		self.games = {}

		self.manager 	= GameManager()
		self.manager.readGames(self.gameDir, 120)
		self.proc	= TargetIo()
							
	def on_message(self, message):
		print "\t", "Message from client: " + message
		data 		= json.loads(lower(message))
		newGame 	= None
		messageOut 	= ""
		if (data.has_key(self.gameQuery)):
			messageOut = u"%s"%(self.manager)
		elif (data.has_key(self.gameStart)):
			# this part starts a new game...
			gameId 	= data[self.gameStart]
			game 	= self.manager.getGame(gameId)
			
			if (game is not None):
			  	messageOut 	= self.jsonTargets(game.targets) 
				newGame 	= game
				
			else:
			  	messageOut = u'{"targets":null}' % (self.gameStart)			
		else:
			# this part starts a 
			messageOut = u"You said this: %s" % (message)
		print "\t"*2, ">> Message Out: ", messageOut
		self.write_message(messageOut)
		if (newGame is not None):
			self.proc.run(newGame, notifier = self.notify)

	def on_close(self):
		print "*** web socket closed ***"
	
	def jsonTargets(self, targets):
		#data 	   = map(lambda x : x.toJson(), targets)
		#targetData = repr(data).replace("'", '"')
		#print targetData
		#data =  u'{"targets": %s}' % (targetData)
		#d = {"targets": targets}
		#return json.dumps(d)		
		return json.dumps(targets, cls=Encoder)
		
	def notify(self, targets):
		messageOut = self.jsonTargets(targets)
		print "\t"*2, "Notifying targets hit", messageOut
		self.write_message("%s" % (messageOut))


class Encoder(json.JSONEncoder):
	def default(self, obj):
		if not isinstance(obj, Target):
			return super(Encoder, self).default(obj)
		return obj.__dict__

def startWeb(port, timeout = 120):
	application = tornado.web.Application([
		(r'/ws', ServerGame),
	])

	http_server = tornado.httpserver.HTTPServer(application)
	http_server.listen(port)
	tornado.ioloop.IOLoop.instance().start()
		

if __name__ == "__main__":
	startWeb(4500, timeout = 120)






