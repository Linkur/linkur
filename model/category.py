__author__ = 'raghothams'

class Category:
	# ID
	# NAME

	def __init__(self):
		self.id = None
		self.name = None

	def __init__(self, id, name):
		self.id = id
		self.name = name

	def __str__(self):
		return {
			'_id' : self.id,
			'name' : self.name
		}