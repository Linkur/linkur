__author__ = 'raghothams'
from model.category import Category

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
				category.id = result["_id"]
				category.name = result["name"]
				category_list.append(category)

			return category_list
		else:
			return None