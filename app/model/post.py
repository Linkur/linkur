
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
	def serialize(self):
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

