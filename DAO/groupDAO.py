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
			group.users = result["users"]
			
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
			group.users = result["users"]

			return group
		else:
			return None


	def insert_group(self, group_obj):
		# do something

		collection = self.collection
		invite_hash = self.createInviteHash()

		if invite_hash != None:
			group_obj.hash = invite_hash
			to_insert = group_obj.db_serializer()
			print to_insert
			result = collection.insert(to_insert)
			
			return result

		else:

			return None

	# generate sharer hash for the group
	def createInviteHash(self):
		invite_hash = None
		try:
			now = datetime.datetime.now()
			now = str(now)
			randno = random.randint(0,99)
			randno = str(randno)

			invite_hash = hashlib.sha1(now+randno).hexdigest()

		except Exception as inst:
			print "error generating invite hash"
			print inst
		
		return invite_hash

	# Append a user to the group document
	def append_user(self, group_obj, user_id):

		collection = self.collection
		result = None

		try:
			result = collection.update({"_id":group_obj.id}, {"$push":{"users":user_id}})
		
		except Exception as inst:
			print inst
			print "Error updating group collection - appending user to group"
			return False

		return True

	# Remove user from group
	def remove_user(self, group_obj, user_id):

		collection = self.collection
		result = None

		try:
			result = collection.update({"_id":group_obj.id}, {"$pull":{"users":user_id}})

		except Exception as inst:
			print inst
			print "Error updating group collection - appending user to group"
			return False

		return True
	