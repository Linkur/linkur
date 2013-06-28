__author__ = 'raghothams'

from flask import Flask
from flask import request
from flask.ext.pymongo import PyMongo
from pymongo import Connection

from DAO.postDAO import PostDAO
from DAO.userDAO import UserDAO
from DAO.sessionDAO import SessionDAO

from model.responseWrapper import ResponseWrapper
from model.post import Post

import json

app = Flask(__name__)
mongo = PyMongo(app)
connection = Connection()

db = connection.sharurl

postDAO = PostDAO(db)
userDAO = UserDAO(db)
sessionDAO = SessionDAO(db)
# @app.route('/')
# def home_page():

@app.route('/singup', methods=['POST'])
def user_signup():
	email = request.form['email']
	password = request.form['password']
	verify = request.form['verify']
	name = request.form['name']

	# set these up in case we have an error case
	errors = {'username': cgi.escape(name), 'email': cgi.escape(email)}
	if validate_signup(name, password, verify, email, errors):

		#create a modelled user
		temp_user = User(email, username, password, batch, user_type)
		if not users.add_user(temp_user):
			# this was a duplicate
			errors['username_error'] = "Username already in use. Please choose another"
			return bottle.template("index", signup_errors = errors, batch_list = result)

		session_id = sessions.start_session(username)
		print session_id
		bottle.response.set_cookie("session", session_id)
		bottle.redirect("/welcome.html")
	else:
		print "user did not validate"
		return bottle.template("index", signup_errors = errors, batch_list = result)


@app.route('/signin', methods=['POST'])
def user_signin():
	username = request.form['username']
	password = request.form['password']

	user_record = userDAO.validate_login(username, password)
	if user_record:
		session_id = sessionDAO.start_session(user_record['_id'])

		if session_id is None:
			return "Internal Error"
		
		cookie = session_id
		response.set_cookie("session",cookie)

		return response
	

@app.route('/posts', methods=['GET'])
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

@app.route('/post', methods=['POST'])
def insert_new_post():

	print 'in poster'
	post = Post()

	form_data = request.form['data']

	json_data = json.loads(form_data)

	post.title = json_data['title']
	post.link = json_data['link']
	post.category = json_data['category']
	post.tags = json_data['tags']
	post.group = json_data['group']

	print post.db_serializer()
	result = postDAO.insert_post(post);
	
	responseWrapper = ResponseWrapper()
	if result != None:
		responseWrapper.set_error(False)
	else:
		responseWrapper.set_error(True)

	return json.dumps(responseWrapper, default=ResponseWrapper.__str__)

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

if __name__ == '__main__':
	app.run(debug=True)

