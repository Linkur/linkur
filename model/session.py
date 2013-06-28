__author__ = 'raghothams'

class Session:
	# ID
	# USERNAME

	def __init__(self):
		self.__id = None
		self.__username = None

	def __init__(self, id, user):
		self.__id = id
		self.__username = user

	def __str__(self):
		return {
			'_id' : self.__id,
			'username' : self.__username
		}
