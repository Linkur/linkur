__author__ = 'raghothams'
#change just to try stash
from flask import Flask
from flask import request
from flask import make_response
from flask.ext.pymongo import PyMongo
from pymongo import Connection

from DAO.postDAO import PostDAO
from DAO.userDAO import UserDAO
from DAO.sessionDAO import SessionDAO
from DAO.categoryDAO import CategoryDAO
from DAO.groupDAO import GroupDAO

from model.responseWrapper import ResponseWrapper
from model.user import User
from model.post import Post
from model.category import Category
from model.group import Group

import json
import cgi
import re


app = Flask(__name__)
mongo = PyMongo(app)
connection = Connection()

db = connection.sharurl

postDAO = PostDAO(db)
userDAO = UserDAO(db)
sessionDAO = SessionDAO(db)
categoryDAO = CategoryDAO(db)
groupDAO = GroupDAO(db)

# @app.route('/')
# def home_page():

@app.route('/signup', methods=['POST'])
def user_signup():
	email = request.form['email']
	password = request.form['password']
	verify = request.form['verify']
	name = request.form['name']

	# set these up in case we have an error case
	errors = {'username': cgi.escape(name), 'email': cgi.escape(email)}
	if validate_signup(name, password, verify, email, errors):

		#create a modelled user
		temp_user = User(email, password, name)
		if not userDAO.add_user(temp_user):
			# this was a duplicate
			errors['username_error'] = "Username already in use. Please choose another"
			# return bottle.template("index", signup_errors = errors, batch_list = result)

		session_id = sessionDAO.start_session(email)
		response = make_response()
		response.set_cookie("session", value=session_id)
		return "signup success"
	else:
		print "user did not validate"
		return "signup fail"
		# return bottle.template("index", signup_errors = errors, batch_list = result)


@app.route('/signin', methods=['POST'])
def user_login():

	username = request.form['email']
	password = request.form['password']

	user_record = userDAO.validate_login(username, password)
	
	if user_record:
		session_id = sessionDAO.start_session(user_record['_id'])

		if session_id is None:
			return "Internal Error"
		
		response = make_response()
		response.set_cookie("session", value=session_id)

		return response
	else:
		return "fail"
	

@app.route('/post', methods=['GET'])
def get_recent_posts():
	
	userid = None
	cookies = request.cookies
	if 'session' in cookies:
		print "cookie : ",cookies['session']
		userid = sessionDAO.get_userid(cookies['session'])  # see if user is logged in
		print "user : ",userid
		user = userDAO.get_user_by_id(userid)
		
		if user != None:
			print request.args
			group_id = None
			try:
				group_id = request.args["groupId"]
			except Exception as inst:
				print "please send groupID as part of url parameter"
				return "GroupID not supplied as URL param"

			posts = postDAO.get_recent_posts(group_id)
			wrapped_response = ResponseWrapper()

			json_result = None

			if posts != None :
				wrapped_response.set_data(posts)
				wrapped_response.set_error(False)
			
			else:
				wrapped_response.set_error(True)
			print(json_result)
			json_result = json.dumps(wrapped_response, default=ResponseWrapper.__str__)

			return 	json_result
		else:
			return "please log in"

	else:
		print "no cookie set"

	

@app.route('/post', methods=['POST'])
def insert_new_post():

	cookie = request.cookies["session"]
	
	print "cookie : ",cookie
	if cookie != None:
		userid = sessionDAO.get_userid(cookie)  # see if user is logged in
		print "user : ",userid

	user = userDAO.get_user_by_id(userid)
	print user.__str__()
	post = Post()

	form_data = request.form['data']

	json_data = json.loads(form_data)

	post.title = json_data['title']
	post.link = json_data['link']
	post.category = json_data['category']
	post.tags = json_data['tags']
	post.group = json_data['groups']
	post.added_by = user.name

	print post.db_serializer()
	result = postDAO.insert_post(post);
	print result
	responseWrapper = ResponseWrapper()
	if result != None:
		responseWrapper.set_error(False)
	else:
		responseWrapper.set_error(True)

	return json.dumps(responseWrapper, default=ResponseWrapper.__str__)

@app.route('/category', methods=['GET'])
def get_categories():

	user = validate_cookie(request)
	if user != None:
		# process things
		result = categoryDAO.get_categories()
		responseWrapper = ResponseWrapper()
		if result != None:
			responseWrapper.set_error(False)
			responseWrapper.set_data(result)
		else:
			responseWrapper.set_error(True)

		return json.dumps(responseWrapper, default=ResponseWrapper.__str__)
	else:
		# redirect to log in screen later
		return "Please sign in"

@app.route('/category', methods=['POST'])
def insert_catergory():
	user = validate_cookie(request)
	if user != None:
		category = Category()

		form_data = request.form['data']
		json_data = json.loads(form_data)
		category.name = json_data['category_name']
		result = categoryDAO.insert_category(category)

		responseWrapper = ResponseWrapper()
		if result != None:
			responseWrapper.set_error(False)
			responseWrapper.set_data(result)
		else:
			responseWrapper.set_error(True)

		return json.dumps(responseWrapper, default=ResponseWrapper.__str__)
	else:
		# TODO redirect to login page
		return "please login"

@app.route('/user/group', methods=['GET'])
def get_user_groups():
	user = validate_cookie(request)
	if user != None:
		groups = userDAO.get_groups(user.id)
		responseWrapper = ResponseWrapper()
		if groups != None:
			responseWrapper.set_error(False)
			responseWrapper.set_data(groups)
		else:
			responseWrapper.set_error(True)

		return json.dumps(responseWrapper, default=ResponseWrapper.__str__)
	else:
		# TODO redirect to login page
		return "please login"

@app.route('/user/group', methods=['POST'])
def append_user_groups():
	user = validate_cookie(request)
	if user != None:
		# TODO
		form_data = request.form['data']
		json_data = json.loads(form_data)
		group = Group()
		group.id = json_data['_id']
		group.name = json_data['group_name']
		result = userDAO.append_group(user.id,group)
		print result
		responseWrapper = ResponseWrapper()
		if result != None:
			responseWrapper.set_error(False)
			responseWrapper.set_data(result)
		else:
			responseWrapper.set_error(True)

		return json.dumps(responseWrapper, default=ResponseWrapper.__str__)

	else:
		# TODO redirect to login page
		return "please login"
	
@app.route('/group', methods=['POST'])
def create_user_groups():
	user = validate_cookie(request)
	if user != None:
		# TODO
		form_data = request.form['data']
		json_data = json.loads(form_data)
		group = Group()
		group.name = json_data['group_name']

		new_group_id = groupDAO.insert_group(group)
		group.id = new_group_id
		result = userDAO.append_group(user.id,group)

		responseWrapper = ResponseWrapper()
		if result != None:
			responseWrapper.set_error(False)
			new_group_id = str(new_group_id)
			print new_group_id
			responseWrapper.set_data([{"group_id":new_group_id}])
		else:
			responseWrapper.set_error(True)

		return json.dumps(responseWrapper, default=ResponseWrapper.__str__)
	else:
		# TODO redirect to login page
		return "please login"

@app.route('/acceptInvite/<invite_hash>', methods=['GET'])
def accept_group_invite(invite_hash):
	# check for cookie
	# check group collection for group id
	# if exists, append group object to table
	# else throw error

	user = validate_cookie(request)
	if user != None:
		group_obj = groupDAO.get_group_by_hash(str(invite_hash))
		if group_obj != None:
			#  check if group is already part for the user
			group_exists = userDAO.does_group_exist(user.id,group_obj)
			print "group exists", group_exists
			result = None
			if group_exists == False:
				result = userDAO.append_group(user.id,group_obj)
			else:
				return "group already part of user"

			responseWrapper = ResponseWrapper()
			if result != None:
				responseWrapper.set_error(False)
				responseWrapper.set_data(result)
			else:
				responseWrapper.set_error(True)

			return json.dumps(responseWrapper, default=ResponseWrapper.__str__)
		else:
			return {"error":True,"data":"Group not found"}
	else:
		# TODO redirect to login page
		return "please login"

# @app.route('/invite/<group_id>', methods=['GET'])
# def generate_group_invite(group_id):

# 	user = validate_cookie(request)
# 	if user != None:
# 		group_obj = groupDAO.get_group_by_id(str(group_id))
# 		if group_obj != None:
# 			invite_url = request.url_root + str(group_id)
# 			return invite_url
# 		else:
# 			return "no such group"
# 	else:
# 		# TODO redirect to login page
# 		return "please login"

# Helper Functions

# validates that the user information is valid for new signup, return True of False
# and fills in the error string if there is an issue
def validate_signup(username, password, verify, email, errors):
    USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
    PASS_RE = re.compile(r"^.{3,20}$")
    EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

    errors['username_error'] = ""
    errors['password_error'] = ""
    errors['verify_error'] = ""
    errors['email_error'] = ""

    if not USER_RE.match(username):
        errors['username_error'] = "invalid username. try just letters and numbers"
        return False

    if not PASS_RE.match(password):
        errors['password_error'] = "invalid password."
        return False
    if password != verify:
        errors['verify_error'] = "password must match"
        return False
    if email != "":
        if not EMAIL_RE.match(email):
            errors['email_error'] = "invalid email address"
            return False
    return True

# validates cookie and check if user is valid
def validate_cookie(request):
	cookie = request.cookies["session"]
	
	print "cookie : ",cookie
	if cookie != None:
		userid = sessionDAO.get_userid(cookie)  # see if user is logged in
		print "user : ",userid
		if userid != None:
			user = userDAO.get_user_by_id(userid)
			print user.__str__()
			if user != None:
				return user
	return None

if __name__ == '__main__':
	app.run(debug=True)

