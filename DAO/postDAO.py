__author__ = 'raghothams'

from model.post import Post

class PostDAO:

	def __init__(self, database):
		self.db = database
		self.recent_collection = self.db.new
		self.achived_collection = self.db.archive

	def get_recent_posts(self, group):
		
		collection = self.recent_collection
		posts = collection.find({
			'group' : group
			})
		
		post_list = self.get_modelled_list(posts)
		return post_list

	def get_archived_posts(self, group):

		collection = self.achived_collection
		posts = collection.find({
			'group' : group
			})

		post_list = self.get_modelled_list(posts)
		return post_list


	def get_modelled_list(self, posts):

		modelled_post_list = []
		for post in posts:

			modelled_post = Post()
			modelled_post.id = post['_id']
			# modelled_post.date = post['date']
			modelled_post.title = post['title']
			modelled_post.link = post['link']
			modelled_post.category = post['category']
			modelled_post.tags = post['tags']
			modelled_post.group = post['group']
			modelled_post.added_by = post['added_by']

			modelled_post_list.append(modelled_post)

		return modelled_post_list

	def insert_post(self, post_obj):

		collection = self.recent_collection

		to_insert = post_obj.db_serializer()
		result = collection.insert(to_insert)

		return result
