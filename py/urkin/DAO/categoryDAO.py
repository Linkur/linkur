__author__ = 'raghothams'
from urkin.model.category import Category
from bson import ObjectId

class CategoryDAO:

	def __init__(self,database):
		self.db = database
		self.categories = self.db.categories

	def get_categories(self):

		collection = self.categories
		results = collection.find()

		if results != None:
			category_list = []
			for result in results:
				print result['name']
				category = Category()
				obj_id = result["_id"]
				category.id = str(obj_id)
				category.name = result["name"]
				category_list.append(category)

			return category_list
		else:
			return None

	def insert_category(self, category_obj):

		collection = self.categories
		to_insert = category_obj.db_serializer()

		result = collection.insert(to_insert)

		return result
