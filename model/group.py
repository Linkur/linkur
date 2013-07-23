__author__ = 'raghothams'

class Group:
	# ID
	# NAME
	# USERS

	def __init__(self):
		self.id = None
		self.name = None
		

	#PARAMS
	#	ID
	# 	GROUP NAME
	
	def __init__(self, id, name):
		self.id = id
		self.name = name

	def __str__(self):
		return {
			'_id' : self.id,
			'name' : self.name
		}

	def db_serializer(self):
		return {
			'name': self.name
		}