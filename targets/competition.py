from sys 	import argv
from local 	import LocalGame
from server 	import startWeb

if __name__ == "__main__":
	isLocal   = False
	if (len(argv) > 1):
		if ("local" in argv):
			isLocal = True

	if (isLocal):
		print "using local game mode"
		local = LocalGame()
		local.start("./games")
	else:
		print "using server game mode"
		startWeb(4500)
	




