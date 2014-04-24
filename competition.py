from sys 	import argv
from local 	import LocalGame
from server 	import startWeb
from targetIo 	import *

if __name__ == "__main__":
	isLocal   = False
	if (len(argv) > 1):
		if ("local" in argv):
			isLocal = True
	
	t = TargetIo()
	t.clearAll(t.pins)
	t.showAll(t.pins)

	if (isLocal):
		print "using local game mode"
		local = LocalGame()
		local.start("./games")
	else:
		print "using server game mode"
		startWeb(4500, timeout = 30)
	




