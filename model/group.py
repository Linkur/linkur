__author__ = 'raghothams'

class Group:
	# ID
	# NAME
	# USERS

	def __init__(self):
		self.id = None
		self.name = None
		self.hash = None
		self.users = []

	def __str__(self):
		return {
			'_id' : self.id,
			'name' : self.name,
			'hash' : self.hash,
			'users' : self.users
		}

	def db_serializer(self):
		return {
			'name': self.name,
			'hash': self.hash,
			'users': self.users
		}