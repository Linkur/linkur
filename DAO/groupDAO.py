__author__ = 'raghothams'
from model.group import Group
from bson import ObjectId

class GroupDAO:

	def __init__(self, database):
		self.db = database
		self.collection = self.db.groups

	def get_group_by_id(self, group_id):
		# get group document from db

		collection = self.collection
		group_id = ObjectId(group_id)
		result = collection.find_one({"_id": group_id});

		if result != None:
			group = Group()
			group.id = group_id
			print group.id
			group.name = result["name"]

			return group
		else:
			return None


	def insert_group(self, group_obj):
		# do something

		collection = self.collection
		to_insert = group_obj.db_serializer()
		result = collection.insert(to_insert)
		print result
		return result
