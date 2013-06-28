__author__ = 'raghothams'

class Group:
	# ID
	# NAME
	# USERS

	def __init__(self):
		self.id = None
		self.name = None
		self.users = []

	#PARAMS
	#	ID
	# 	GROUP NAME
	# 	LIST OF USERS or None
	# 		i.e pass list of user objects or None
	def __init__(self, id, name, users):
		self.id = id
		self.name = name
		if users != None:
			self.users = users

	def __str__(self):
		return {
			'_id' : self.id,
			'name' : self.name,
			'users' : self.users
		}