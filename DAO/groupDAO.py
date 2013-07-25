__author__ = 'raghothams'
from model.group import Group
from bson import ObjectId
import hashlib
import random
import datetime

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
			# print group.id
			group.name = result["name"]
			group.hash = result["hash"]

			return group
		else:
			return None

	def get_group_by_hash(self, invite_hash):

		collection = self.collection
		result = collection.find_one({"hash": invite_hash});

		if result != None:
			group = Group()
			group.id = result["_id"]
			# print group.id
			group.name = result["name"]
			group.hash = result["hash"]

			return group
		else:
			return None


	def insert_group(self, group_obj):
		# do something

		collection = self.collection
		invite_hash = createInviteHash()

		if invite_hash != None:

			to_insert = group_obj.db_serializer()
			result = collection.insert(to_insert)
			print result
			return result

		else:

			return None

	def createInviteHash(self):
		invite_hash = None
		try:
			now = datetime.datetime.now()
			now = str(now)
			randno = random.randint(0,99)
			randno = str(randno)

			invite_hash = hashlib.sha256(now+randno).hexdigest()

		except Exception as inst:
			print "error generating invite hash"
			print inst
		
		return invite_hash

