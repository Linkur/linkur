import json

class ResponseWrapper:

	def __init__(self):
		self.data = []
		self.error = False
		# self.typeinfo = None

	def set_data(self, data):
		self.data = data
		# self.typeinfo = classname

	def set_error(self, error):
		self.error = error

	def get_stringified_data(self):
		results = []
		if len(self.data) > 0 :
			for item in self.data:
				serialized = item.__str__()
				results.append(serialized)
			return results
		else:
			return ""

	def __str__(self):
		
		jsoned = {
					'error' : self.error,
					# 'data' : json.dumps(self.data, default=json_util.default)
					'data' : self.get_stringified_data()
				}
		
		return jsoned