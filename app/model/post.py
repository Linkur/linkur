
import uuid
import datetime
	# ID
	# DATE
	# TITLE
	# LINK
	# CATEGORY (categoryid) optional
	# TAGS
	# GROUP (groupid)
	# ADDED BY USER (username)

class Post:

	def __init__(self):
		self.id = None
		self.date = None
		self.title = None
		self.link = None
		self.category = None
		self.tags = None
		self.group = None
		self.added_by = None

	# Use this to serialize the DB output
	def __str__(self):
		return {
			"_id" : str(self.id),
			"date" : str(self.date),
			"title" : self.title,
			"link" : self.link,
			"category" : self.category,
			"tags" : self.tags,
			"group" : str(self.group),
			"added_by" : str(self.added_by)
		}

	# Use this to serialize the DB input
	def db_serializer(self):
		return {
			"date" : datetime.datetime.utcnow(),
			"title" : self.title,
			"link" : self.link,
			"category" : self.category,
			"tags" : self.tags,
			"group" : self.group,
			"added_by" : self.added_by
		}
