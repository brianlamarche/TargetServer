class GroupConfig:
	def __init__(self, name):
		self.configs = []
		self.totalPoints = 0
		self.name = name

	def calculatePoints():
		totalPoints = 0
		for config in configs:
			totalPoints = totalPoints + config.calculatePoints()
		self.totalPoints = totalPoints
		return totalPoints
	
