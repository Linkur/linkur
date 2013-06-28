__author__ = 'raghothams'

class Session:
	# ID
	# USERNAME

	def __init__(self):
		self.id = None
		self.username = None


	def __str__(self):
		return {
			'_id' : self.__id,
			'userid' : self.__userid
		}
