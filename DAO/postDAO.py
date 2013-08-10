__author__ = 'raghothams'

from model.post import Post
import datetime
from bson import ObjectId

class PostDAO:

	def __init__(self, database):
		self.db = database
		self.recent_collection = self.db.new
		self.achived_collection = self.db.archive

	def get_recent_posts(self, groupid):
		
		posts = None
		try:
			groupid = ObjectId(groupid)
			collection = self.recent_collection
			posts = collection.find({
				'group' : groupid
				})
			print 'posts - ', posts
		except Exception as inst:
			print "error reading recent posts"
			print inst

		if posts != None:
			post_list = self.get_modelled_list(posts)
			print 'LOL'
			print post_list
			return post_list
		else:
			return None

	def get_archived_posts(self, groupid):

		posts = None
		try:
			groupid = ObjectId(groupid)
			collection = self.achived_collection
			posts = collection.find({
				'group' : groupid
				})

		except Exception as inst:
			print "error reading recent posts"
			print inst

		if posts != None:
			post_list = self.get_modelled_list(posts)
			return post_list
		else:
			return None

	def searchTitle(self, queryText):
		modelled_search_results = None
		collection = self.recent_collection

		for query in queryText:
			# print query
			try:
				results = collection.find({
					'title': query
					})

				if results != None:
					intermediate_result = self.get_modelled_list(results)
					print "interim result", intermediate_result
					if modelled_search_results == None:
						modelled_search_results = intermediate_result
					else:
						modelled_search_results = modelled_search_results + intermediate_result

			except Exception as inst:
				print "error processing search"
				print inst
				return None
		print "final result title", modelled_search_results
		return modelled_search_results

	def searchTags(self, queryText):
		modelled_search_results = None
		collection = self.recent_collection
		
		for query in queryText:

			try:
				results = collection.find({
					"tags": {
						"$in":[query]
					}
				})

				if results != None:
					intermediate_result = self.get_modelled_list(results)
					
					if modelled_search_results == None:
						modelled_search_results = intermediate_result
					else:
						modelled_search_results = modelled_search_results + intermediate_result


			except Exception as inst:
				print "error processing search"
				print inst
				return None
		
		return modelled_search_results

	def search(self, queryText):
		posts = None
		queryText = queryText.split()
		# search for title field for query text
		title_results = self.searchTitle(queryText)
		if title_results != None:
			posts = title_results
		
		# search for tags array for query text
		tags_results = self.searchTags(queryText)
		if tags_results != None:
			if posts != None:
				posts = posts + tags_results
			else:
				posts = tags_results

		return posts

	def get_modelled_list(self, posts):

		modelled_post_list = []
		for post in posts:
			try:
				modelled_post = Post()
				modelled_post.id = post['_id']

				date_obj = post['date']
				modelled_post.date = date_obj.isoformat()
				# print post['title']
				modelled_post.title = post['title']
				modelled_post.link = post['link']
				modelled_post.category = post['category']
				modelled_post.tags = post['tags']
				modelled_post.group = post['group']
				modelled_post.added_by = post['added_by']
				# print modelled_post.title
				modelled_post_list.append(modelled_post)
				# print "in", modelled_post_list

			except Exception as inst:
				print "error processing objects"
				print inst
				return None
		# print "out", modelled_post_list
		return modelled_post_list

	def insert_post(self, post_obj):

		collection = self.recent_collection
		result = None
		try:
			to_insert = post_obj.db_serializer()
			# print to_insert
			result = collection.insert(to_insert)
		except Exception as inst:
			print "error writing post"
			print inst

		return result
