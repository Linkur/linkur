__author__ = 'raghothams'

from flask import Flask
from flask.ext.pymongo import PyMongo
from pymongo import Connection

from DAO.postDAO import PostDAO
from DAO.userDAO import UserDAO

from model.responseWrapper import ResponseWrapper
import json

app = Flask(__name__)
mongo = PyMongo(app)
connection = Connection()

db = connection.sharurl

postDAO = PostDAO(db)
userDAO = UserDAO(db)
# @app.route('/')
# def home_page():
	

@app.route('/posts/', methods=['GET'])
def get_recent_posts():
	
	user = userDAO.get_user_by_id('tester')
	groups = user['groups']
	posts = postDAO.get_recent_posts(groups[0])
	wrapped_response = ResponseWrapper()

	json_result = None

	if posts != None :
		wrapped_response.set_data(posts)
		wrapped_response.set_error(False)
		json_result = json.dumps(wrapped_response, default=ResponseWrapper.__str__)
	
	else:
		wrapped_response.set_error(True)
		json_result = json.dumps(wrapped_response, default=ResponseWrapper.__str__)

	return 	json_result

if __name__ == '__main__':
	app.run(debug=True)

