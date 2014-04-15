import json, types
from target 	import *
from string  	import *
	
def ConvertTargetsToJson(targets):
	return json.dumps(targets, cls=Encoder)
		

class Encoder(json.JSONEncoder):
	def default(self, obj):
		if not isinstance(obj, Target):
			return super(Encoder, self).default(obj)
		return obj.__dict__

		







