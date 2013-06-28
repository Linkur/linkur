__author__ = 'raghothams'

class User:
	# EMAIL
	# PASSWORD
	# NAME
	# GROUPS (COPY)

	def __init__(self, email, password, name):
		self.id = email
		self.password = password
		self.name = name

	def __str__(self):
		return {
			'_id' : self.id,
			'password' : self.password,
			'name' : self.name,
			'groups' : self.groups
		}

	def db_serializer(self):
		return {
			'_id' : self.id,
			'password' : self.password,
			'name' : self.name,
			'groups' : []
		}