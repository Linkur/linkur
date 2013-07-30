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
import sys


app = Flask(__name__)
mongo = connection = db = None
try:
	mongo = PyMongo(app)
	connection = Connection()
	db = connection.sharurl
except Exception as inst:
	print "Error connecting to mongo db server"
	print inst
	sys.exit(-1)

if db != None:
	postDAO = PostDAO(db)
	userDAO = UserDAO(db)
	sessionDAO = SessionDAO(db)
	categoryDAO = CategoryDAO(db)
	groupDAO = GroupDAO(db)

# @app.route('/')
# def home_page():

@app.route('/signup', methods=['POST'])
def user_signup():
	email = None
	password = None
	name = None
	responseWrapper = ResponseWrapper()
	response = make_response()

	try:
		email = request.form['email']
		password = request.form['password']
		name = request.form['name']
	except Exception as inst:
		print "error reading form values"
		responseWrapper.set_error(True)
		responseWrapper.set_data(errors)
		response.data = json.dumps(responseWrapper, default=ResponseWrapper.__str__)
		response.mimetype = "application/json"
		return response

	if email != None and password != None and name != None:

		# set these up in case we have an error case
		errors = {'username': cgi.escape(name), 'email': cgi.escape(email)}
		
		if validate_signup(name, password, email, errors):

			#create a modelled user
			temp_user = User(email, password, name)
			if not userDAO.add_user(temp_user):
				# this was a duplicate
				errors['username_error'] = "Username already in use. Please choose another"
				responseWrapper.set_error(True)
				responseWrapper.set_data(errors)
				response.data = json.dumps(responseWrapper, default=ResponseWrapper.__str__)
				response.mimetype = "application/json"
				return response

			session_id = sessionDAO.start_session(email)			
			response.set_cookie("session", value=session_id)

			responseWrapper.set_error(False)
			responseWrapper.set_data(["User Signup success!"])

		else:
			
			print "user did not validate"
			responseWrapper.set_error(True)
			responseWrapper.set_data(["User did not validate. Signup failed!"])

	else:
		
		responseWrapper.set_error(True)
		responseWrapper.set_data(["Error in form data"])

	response.data = json.dumps(responseWrapper, default=ResponseWrapper.__str__)
	response.mimetype = "application/json"
	return response


@app.route('/signin', methods=['POST'])
def user_login():

	username = request.form['email']
	password = request.form['password']

	user_record = userDAO.validate_login(username, password)
	responseWrapper = ResponseWrapper()
	response = make_response()
	
	if user_record:
		session_id = sessionDAO.start_session(user_record['_id'])

		if session_id is None:
			responseWrapper.set_error(True)
			responseWrapper.set_data(["Session not found. Signin again"])
			response.data = json.dumps(responseWrapper, default=ResponseWrapper.__str__)
			response.mimetype = "application/json"
			return response
		
		response.set_cookie("session", value=session_id)

		responseWrapper.set_error(False)
		

	else:
		responseWrapper.set_error(True)
		responseWrapper.set_data(["User not found"])
	
	response.data = json.dumps(responseWrapper, default=ResponseWrapper.__str__)
	response.mimetype = "application/json"
	return response

@app.route('/logout')
def process_signout():
	cookies = request.cookies
	responseWrapper = ResponseWrapper()
	response = make_response()

	if 'session' in cookies:
		print "cookie : ",cookies['session']
		userid = sessionDAO.get_userid(cookies['session'])  # see if user is logged in
		print "user : ",userid
	sessionDAO.end_session(cookies['session'])
	
	responseWrapper.set_error(False)
	responseWrapper.set_data(["Signed out"])
	
	response.set_cookie("session", value="")
	response.data = json.dumps(responseWrapper, default=ResponseWrapper.__str__)
	response.mimetype = "application/json"

	return response


@app.route('/post', methods=['GET'])
def get_recent_posts():
	
	userid = None
	cookies = request.cookies
	responseWrapper = ResponseWrapper()
	response = make_response()

	if 'session' in cookies:
		print "cookie : ",cookies['session']
		userid = sessionDAO.get_userid(cookies['session'])  # see if user is logged in
		print "user : ",userid
		user = userDAO.get_user_by_id(userid)
		
		if user != None:
			group_id = None
			try:
				group_id = request.args["groupId"]
				print group_id
			except Exception as inst:
				print "please send groupID as part of url parameter"
				responseWrapper.set_error(True)
				responseWrapper.set_data(["GroupID not supplied as URL param"])
				response.data = json.dumps(responseWrapper, default=ResponseWrapper.__str__)
				response.mimetype = "application/json"
				return response

			posts = postDAO.get_recent_posts(group_id)

			json_result = None

			if posts != None :
				responseWrapper.set_data(posts)
				responseWrapper.set_error(False)
			
			else:
				responseWrapper.set_error(True)
			print(json_result)

		else:
			responseWrapper.set_error(True)
			responseWrapper.set_data(["User not found"])

	else:
		responseWrapper.set_error(True)
		responseWrapper.set_data(["User not logged in"])
		
		# redirect("/index.html")
	response.data = json.dumps(responseWrapper, default=ResponseWrapper.__str__)
	response.mimetype = "application/json"
	return response


@app.route('/user/info', methods=['GET'])
def get_userinfo():
	userid = None
	cookies = request.cookies
	responseWrapper = ResponseWrapper()
	response = make_response()

	if 'session' in cookies:
		print "cookie : ",cookies['session']
		userid = sessionDAO.get_userid(cookies['session'])  # see if user is logged in
		print "user : ",userid
		user = userDAO.get_user_info(userid)

		if user != None:
			responseWrapper.set_data([user])
			responseWrapper.set_error(False)
		else:
			responseWrapper.set_error(True)
			responseWrapper.set_data(["User not found. Please Login"])
		
	else:
		responseWrapper.set_error(True)
		responseWrapper.set_data(["User not logged in. Please Login"])
	
	response.data = json.dumps(responseWrapper, default=ResponseWrapper.__str__)
	response.mimetype = "application/json"
	return response


@app.route('/post', methods=['POST'])
def insert_new_post():

	responseWrapper = ResponseWrapper()
	response = make_response()

	cookie = request.cookies["session"]
	print "cookie : ",cookie

	if cookie != None:
		userid = sessionDAO.get_userid(cookie)  # see if user is logged in
		print "user : ",userid

		user = userDAO.get_user_by_id(userid)
		print user.__str__()
		post = Post()
		
		try:
			# build post object from form data
			form_data = request.form['data']
			json_data = json.loads(form_data)
			
			post.title = json_data['title']
			post.link = json_data['link']
			post.category = json_data['category']
			post.tags = json_data['tags']
			post.group = json_data['groups']
			post.added_by = user.name

		except Exception as inst:
			print "error reading form data"
			print inst
			responseWrapper = ResponseWrapper()
			responseWrapper.set_error(True)
			responseWrapper.set_data(["error reading form data. Retry posting"])

		if post.title != None and post.link != None and post.group != None and post.added_by != None:

			result = postDAO.insert_post(post);
			responseWrapper = ResponseWrapper()
			if result != None:
				responseWrapper.set_error(False)
			else:
				responseWrapper.set_error(True)

		else:
			print "error in form data"
			responseWrapper = ResponseWrapper()
			responseWrapper.set_error(True)
			responseWrapper.set_data(["insufficient fields, try again"])
	else:
		responseWrapper.set_error(True)
		responseWrapper.set_data(["User not logged in. Please Login"])

	response.data = json.dumps(responseWrapper, default=ResponseWrapper.__str__)
	response.mimetype = "application/json"
	return response

@app.route('/category', methods=['GET'])
def get_categories():

	user = validate_cookie(request)
	responseWrapper = ResponseWrapper()
	response = make_response()

	if user != None:
		# process things
		result = categoryDAO.get_categories()
		if result != None:
			responseWrapper.set_error(False)
			responseWrapper.set_data([result])
		else:
			responseWrapper.set_error(True)
			responseWrapper.set_data(["error reading categories"])

	else:
		responseWrapper.set_error(True)
		responseWrapper.set_data(["User not found. Please login again"])
	
	response.data = json.dumps(responseWrapper, default=ResponseWrapper.__str__)
	response.mimetype = "application/json"
	return response

@app.route('/category', methods=['POST'])
def insert_catergory():
	user = validate_cookie(request)
	responseWrapper = ResponseWrapper()
	response = make_response()

	if user != None:
		category = Category()

		form_data = request.form['data']
		json_data = json.loads(form_data)
		category.name = json_data['category_name']
		result = categoryDAO.insert_category(category)

		if result != None:
			responseWrapper.set_error(False)
			responseWrapper.set_data(result)
		else:
			responseWrapper.set_error(True)
			responseWrapper.set_data(["error writing category"])

	else:
		responseWrapper.set_error(True)
		responseWrapper.set_data(["User not found. Please login again"])

	response.data = json.dumps(responseWrapper, default=ResponseWrapper.__str__)
	response.mimetype = "application/json"
	return response


@app.route('/user/group', methods=['GET'])
def get_user_groups():
	user = validate_cookie(request)
	responseWrapper = ResponseWrapper()
	response = make_response()

	if user != None:
		groups = userDAO.get_groups(user.id)		
		if groups != None:
			responseWrapper.set_error(False)
			responseWrapper.set_data(groups)
		else:
			responseWrapper.set_error(True)
			responseWrapper.set_data(["error reading user groups"])

	else:
		responseWrapper.set_error(True)
		responseWrapper.set_data(["User not found. Please login again"])

	response.data = json.dumps(responseWrapper, default=ResponseWrapper.__str__)
	response.mimetype = "application/json"
	return response

# @app.route('/user/group', methods=['POST'])
# def append_user_groups():
	
# 	user = validate_cookie(request)
# 	responseWrapper = ResponseWrapper()
# 	response = make_response()

# 	if user != None:
		
# 		group = Group()
# 		try:
# 			form_data = request.form['data']
# 			json_data = json.loads(form_data)
# 			group.id = json_data['_id']
# 			group.name = json_data['group_name']
# 		except Exceptionas inst:
# 			print "error reading form data"
# 			responseWrapper.set_error(True)
# 			responseWrapper.set_data([str(inst)])
# 			response.data = json.dumps(responseWrapper, default=ResponseWrapper.__str__)
# 			response.mimetype = "application/json"
# 			return response

# 		result = userDAO.append_group(user.id,group)
		
# 		if result != None:
# 			responseWrapper.set_error(False)
# 			responseWrapper.set_data(result)
# 		else:
# 			responseWrapper.set_error(True)
# 			responseWrapper.set_data(["error writing user groups"])

# 	else:
# 		responseWrapper.set_error(True)
# 		responseWrapper.set_data(["User not found. Please login again"])

# 	response.data = json.dumps(responseWrapper, default=ResponseWrapper.__str__)
# 	response.mimetype = "application/json"
# 	return response
	
# create a new group. On success of new group creation, the group is automatically appended to the user
@app.route('/group', methods=['POST'])
def create_user_groups():
	user = validate_cookie(request)
	responseWrapper = ResponseWrapper()
	response = make_response()

	if user != None:
		
		group = Group()
		try:
			form_data = request.form['data']
			json_data = json.loads(form_data)
			group.name = json_data['group_name']

		except Exception as inst:
			print "Error reading form data"
			responseWrapper.set_error(True)
			responseWrapper.set_data([inst])
			response.data = json.dumps(responseWrapper, default=ResponseWrapper.__str__)
		 	response.mimetype = "application/json"
		 	return response

		new_group_id = groupDAO.insert_group(group)
		group.id = new_group_id
		result = userDAO.append_group(user.id,group)

		if result != None:
			responseWrapper.set_error(False)
			new_group_id = str(new_group_id)
			responseWrapper.set_data([{"group_id":new_group_id}])
		else:
			responseWrapper.set_error(True)
			responseWrapper.set_data(["error writing group"])

	else:
		responseWrapper.set_error(True)
		responseWrapper.set_data(["User not found. Please login again"])
	
	response.data = json.dumps(responseWrapper, default=ResponseWrapper.__str__)
	response.mimetype = "application/json"
	return response

@app.route('/acceptInvite/<invite_hash>', methods=['GET'])
def accept_group_invite(invite_hash):
	# check for cookie
	# check group collection for group id
	# if exists, append group object to table
	# else throw error

	user = validate_cookie(request)
	responseWrapper = ResponseWrapper()
	response = make_response()

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
				responseWrapper.set_error(False)
				responseWrapper.set_data(["group already part of user"])

			responseWrapper = ResponseWrapper()
			if result != None:
				responseWrapper.set_error(False)
				responseWrapper.set_data(result)
			else:
				responseWrapper.set_error(True)
				responseWrapper.set_data(["error adding group to user"])

		else:
			responseWrapper.set_error(True)
			responseWrapper.set_data(["No such group. Try again"])
	else:
		# TODO redirect to login page
		responseWrapper.set_error(True)
		responseWrapper.set_data(["User not found. Please login again"])
	
	response.data = json.dumps(responseWrapper, default=ResponseWrapper.__str__)
	response.mimetype = "application/json"
	return response

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
def validate_signup(username, password, email, errors):
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
    # if password != verify:
    #     errors['verify_error'] = "password must match"
    #     return False
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

