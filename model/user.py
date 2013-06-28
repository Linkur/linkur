__author__ = 'raghothams'

class User:
	# EMAIL
	# PASSWORD
	# NAME
	# GROUPS (COPY)

	def __init__(self):
		self.id = None
		self.password = None
		self.name = None
		self.groups = []

	#PARAMS
	#	EMAILID
	#	PASSWORD
	#	LIST OF GROUPS THE USER BELONGS TO or None
	# 		i.e pass list of group objects or None
	def __init__(self, id, password, name, groups):
		self.id = id
		self.password = password
		self.name = name

		if groups != None:
			self.groups = groups

	def __str__(self):
		return {
			'_id' : self.id,
			'password' : self.password,
			'name' : self.name,
			'groups' : self.groups
		}