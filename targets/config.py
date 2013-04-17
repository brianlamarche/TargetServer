class Config:
	def __init__(self, targets, name, groupName, t):
		self.name      	 = name
		self.targets   	 = targets
		self.groupName 	 = groupName
		self.totalTime   = t 
		self.totalHits 	 = 0
		self.elapsedTime = 0
