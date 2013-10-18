__author__ = 'raghothams'
#change just to try stash
from flask import Flask
from flask import request
from flask import make_response
from flask import redirect
from decorator import crossdomain
from flask.ext.pymongo import PyMongo
from pymongo import Connection
from bson import ObjectId

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


# API for user registration
@app.route('/signup', methods=['POST'])
def user_signup():
    email = None
    password = None
    name = None
    responseWrapper = ResponseWrapper()
    response = any_response(request)
    print request.form
    email = request.form['email']
    password = request.form['password']
    name = request.form['name']
    verify = request.form['verify']

    if email != None and password != None and name != None:

        # set these up in case we have an error case
        errors = {'username': cgi.escape(name), 'email': cgi.escape(email)}

        if validate_signup(name, password, verify, email, errors):

            #create a modelled user
            temp_user = User(email, password, name)
            if not userDAO.add_user(temp_user):
                # this was a duplicate
                errors['username_error'] = "Username already in use. Please choose another"
                responseWrapper.set_error(True)
                responseWrapper.set_data(errors)
                response.data = json.dumps(responseWrapper, default=ResponseWrapper.__str__)
                response.mimetype = "application/json"
                response.status_code = 400
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

# API for user signin
@crossdomain(origin='http://localhost:8000', methods=['OPTIONS', 'POST'])
@app.route('/signin', methods=['POST','OPTIONS'])
def user_login():

    responseWrapper = ResponseWrapper()
    response = any_response(request)
    username = None
    password = None

    try:
        username = request.form['email']
        print username
        password = request.form['password']
        print password

    except Exception as inst:
        print "error reading form data"
        print inst
        responseWrapper.set_error(True)
        responseWrapper.set_data(["Error reading form data. check form data"])
        response.data = json.dumps(responseWrapper, default=ResponseWrapper.__str__)
        response.mimetype = "application/json"
        return response

    if username != None and password != None:
        validation_result = userDAO.validate_login(username, password)
        if validation_result["error"] == True:
            # error
            responseWrapper.set_error(True)
            responseWrapper.set_data(validation_result["data"])

        else:
            # continue processing
            user_record = validation_result["data"]

            if user_record:
                session_id = sessionDAO.start_session(user_record['_id'])

                if session_id is None:
                    responseWrapper.set_error(True)
                    responseWrapper.set_data(["Session not found. Signin again"])
                    response.data = json.dumps(responseWrapper, default=ResponseWrapper.__str__)
                    response.mimetype = "application/json"
                    return response
                # set_cookie(key, value='', max_age=None, expires=None, path='/', domain=None, secure=None, httponly=False)
                response.set_cookie("session", value=session_id, expires=None, path="/", httponly=True)

                responseWrapper.set_error(False)	
                responseWrapper.set_data(["Signin success"])		

            else:
                responseWrapper.set_error(True)
                responseWrapper.set_data(["User not found"])
    else:
        responseWrapper.set_error(True)
        responseWrapper.set_data(["Username / password blank"])

    response.data = json.dumps(responseWrapper, default=ResponseWrapper.__str__)
    response.mimetype = "application/json"
    return response

# API for user session logout
@app.route('/logout', methods=['POST', 'OPTIONS'])
def process_signout():
   
    cookies = request.cookies
    print cookies
    responseWrapper = ResponseWrapper()
    response = any_response(request)

    if 'session' in cookies:
        print "cookie : ",cookies['session']
        userid = sessionDAO.get_userid(cookies['session'])  # see if user is logged in
        print "user : ",userid
        
        if userid != None:
            sessionDAO.end_session(cookies['session'])
            
            response.status_code = 200
            return response
        else:
            responseWrapper.set_error(True)
            responseWrapper.set_data(["User not found"])
            response.status_code = 302
    else:
        responseWrapper.set_error(True)
        responseWrapper.set_data(["User not logged in"])
        response.status_code = 302

    response.set_cookie("session", value="None")
    response.data = json.dumps(responseWrapper, default=ResponseWrapper.__str__)
    response.mimetype = "application/json"

    return response

# API to change user password
@app.route('/user/password', methods=['POST', 'OPTIONS'])
def change_user_password():

    responseWrapper = ResponseWrapper()
    response = any_response(request)
    user = validate_cookie(request)

    if user != None:

        # read form data for old & new password
        try:
            old_password = request.form['old_password']
            print old_password

            new_password = request.form['new_password']
            print new_password

            result = userDAO.change_password(user.id, old_password, new_password)

            if result != None:
                # update success
                responseWrapper.set_data(["Success updating password"])
                responseWrapper.set_error(False)
            
            else:
                # update FAILURE
                responseWrapper.set_data(["Error updating password"])
                responseWrapper.set_error(True)
        except Exception as inst:
            print "An error occurred while updating password"
            print inst

    else:
        responseWrapper.set_error(True)
        responseWrapper.set_data(["User not found"])
        response.status_code = 302

    response.data = json.dumps(responseWrapper, default=ResponseWrapper.__str__)
    response.mimetype = "application/json"
    return response


# API for reading all posts for a given group
@app.route('/post', methods=['GET', 'OPTIONS'])
def get_recent_posts():

    responseWrapper = ResponseWrapper()
    response = any_response(request)
    user = validate_cookie(request)

    if user != None:
        group_id = None
        try:
            group_id = request.args["group_id"]
            print group_id
        except Exception as inst:
            print "please send group_id as part of url parameter"
            responseWrapper.set_error(True)
            responseWrapper.set_data(["group_id not supplied as URL param"])
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
        response.status_code = 302

        # redirect("/index.html")
    response.data = json.dumps(responseWrapper, default=ResponseWrapper.__str__)
    response.mimetype = "application/json"
    return response


# API for searching posts with given keywords
@app.route('/search', methods=['GET','OPTIONS'])
def search():

    responseWrapper = ResponseWrapper()
    response = any_response(request)
    user = validate_cookie(request)
    print user.__str__()

    if user != None:
        queryText = request.args["q"]
        # print queryText
        result = postDAO.search(user, queryText)
        response = any_response(request)

        responseWrapper.set_data(result)
        responseWrapper.set_error(False)

    else:
        responseWrapper.set_error(True)
        responseWrapper.set_data(["User not found, Login"])
        response.status_code = 302

    response.data = json.dumps(responseWrapper, default=ResponseWrapper.__str__)
    response.mimetype = "application/json"
    return response



# API for reading user info
@app.route('/user/info', methods=['GET', 'OPTIONS'])
def get_userinfo():
    
    responseWrapper = ResponseWrapper()
    response = any_response(request)
    user = validate_cookie(request)

    if user != None:
        user = userDAO.get_user_info(user.id)
        responseWrapper.set_data([user])
        responseWrapper.set_error(False)
    else:
        responseWrapper.set_error(True)
        responseWrapper.set_data(["User not found. Please Login"])
        response.status_code = 302

    response.data = json.dumps(responseWrapper, default=ResponseWrapper.__str__)
    response.mimetype = "application/json"
    return response


# API for creating new post
@app.route('/post', methods=['PUT'])
def insert_new_post():

    responseWrapper = ResponseWrapper()
    response = any_response(request)
    
    user = validate_cookie(request)
    
    if user != None:
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
                responseWrapper.set_data([str(result)])
                response.status_code = 201

            else:
                responseWrapper.set_error(True)
                responseWrapper.set_data(["error writing post"])

        else:
            print "error in form data"
            responseWrapper = ResponseWrapper()
            responseWrapper.set_error(True)
            responseWrapper.set_data(["insufficient fields, try again"])
            response.status_code = 302
    else:
        responseWrapper.set_error(True)
        responseWrapper.set_data(["User not logged in. Please Login"])
        response.status_code = 302

    response.data = json.dumps(responseWrapper, default=ResponseWrapper.__str__)
    response.mimetype = "application/json"
    
    return response

# API for deleting a post
@app.route('/post/<post_id>', methods=['DELETE', 'OPTIONS'])
def delete_post(post_id=None):
    responseWrapper = ResponseWrapper()
    response = any_response(request)

    user = validate_cookie(request)
    
    if user != None:
        if post_id != None:
                        
            try:
                result = postDAO.delete_post(post_id)
                print "result is ", result

                if result == None:
                    responseWrapper.set_error(True)
                    responseWrapper.set_data(["Error deleting post"])
                else:
                    responseWrapper.set_error(False)
                    responseWrapper.set_data(["Success deleting post"])
                    response.status_code = 200

            except Exception as inst:
                print inst
                responseWrapper.set_error(True)
                responseWrapper.set_data(["Error deleting post"])
                response.status_code = 500
        else:
            responseWrapper.set_error(True)
            responseWrapper.set_data(["Post id is null"])

    else:
        responseWrapper.set_error(True)
        responseWrapper.set_data(["User not logged in. Please Login"])
        response.status_code = 302

    response.data = json.dumps(responseWrapper, default=ResponseWrapper.__str__)
    response.mimetype = "application/json"
    
    return response

# API for reading categories
@app.route('/category', methods=['GET'])
def get_categories():

    user = validate_cookie(request)
    responseWrapper = ResponseWrapper()
    response = any_response(request)

    if user != None:
        # process things
        result = categoryDAO.get_categories()
        if result != None:
            responseWrapper.set_error(False)
            responseWrapper.set_data([result])
        else:
            responseWrapper.set_error(True)
            responseWrapper.set_data(["error reading categories"])
            response.status_code = 302

    else:
        responseWrapper.set_error(True)
        responseWrapper.set_data(["User not found. Please login again"])
        response.status_code = 302

    response.data = json.dumps(responseWrapper, default=ResponseWrapper.__str__)
    response.mimetype = "application/json"
    return response

# API for adding category
@app.route('/category', methods=['POST'])
def insert_catergory():
    user = validate_cookie(request)
    responseWrapper = ResponseWrapper()
    response = any_response(request)

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
        response.status_code = 302

    response.data = json.dumps(responseWrapper, default=ResponseWrapper.__str__)
    response.mimetype = "application/json"
    return response


# API for reading user groups
@app.route('/user/group', methods=['GET', 'OPTIONS'])
def get_user_groups():
    user = validate_cookie(request)
    responseWrapper = ResponseWrapper()
    response = any_response(request)

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
        response.status_code = 302

    response.data = json.dumps(responseWrapper, default=ResponseWrapper.__str__)
    response.mimetype = "application/json"
    return response

# API for creating new group. On success of new group creation, the group is automatically appended to the user
@app.route('/group', methods=['POST', 'OPTIONS'])
def create_user_groups():

    user = validate_cookie(request)
    print user.__str__()
    responseWrapper = ResponseWrapper()

    print "hello new group"
    response = any_response(request)

    if user != None:

        group = Group()
        try:
            # form_data = request.form['data']
            print request.form
            form_data = request.form['data']
            json_data = json.loads(form_data)
            group.name = json_data['group_name']
            print "appending to group user ", user.id
            group.users.append(user.id)

        except Exception as inst:
            print inst
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
        response.status_code = 302

    response.data = json.dumps(responseWrapper, default=ResponseWrapper.__str__)
    response.mimetype = "application/json"
    return response

# API for removing a user from a group
@app.route('/group/<group_id>', methods = ['OPTIONS', 'DELETE'])
def remove_group_for_user(group_id=None):
    # check for cookie & get user object
    # check group collection for group id
    # if exists, remove user from group collection
    # then remove group from user collection
    # else throw error

    user = validate_cookie(request)
    responseWrapper = ResponseWrapper()
    response = any_response(request)

    if user != None:
        
        if group_id != None:
            group_obj = groupDAO.get_group_by_id(str(group_id))
        
            if group_obj != None:
                #  check if group is already part for the user
                group_exists = userDAO.does_group_exist(user.id,group_obj)
                print "group exists", group_exists
                remove_group_result = None
                remove_user_result = None

                if group_exists == True:
                    remove_group_result = groupDAO.remove_user(group_obj, user.id)
                    # TODO if the group contains ZERO number of users, delete group
                    remove_user_result = userDAO.remove_group(user.id, group_obj)

                else:
                    print "Group not related to user"

                # check for DB errors
                if remove_group_result != False and remove_user_result != False:
                    responseWrapper.set_error(False)
                    responseWrapper.set_data(["Success removing group"])
                
                elif remove_user_result == False:
                    responseWrapper.set_error(True)
                    responseWrapper.set_data(["error removing group from user"])
                
                else:
                    responseWrapper.set_error(True)
                    responseWrapper.set_data(["error removing user from group"])

            else:
                responseWrapper.set_error(True)
                responseWrapper.set_data(["No such group. Try again"])
        else:
            responseWrapper.set_error(True)
            responseWrapper.set_data(["group id is null"])
    else:
        # TODO redirect to login page
        responseWrapper.set_error(True)
        responseWrapper.set_data(["User not found. Please login again"])
        response.status_code = 302

    response.data = json.dumps(responseWrapper, default=ResponseWrapper.__str__)
    response.mimetype = "application/json"
    return response


# API for joining a user to a group
@app.route('/group/join/<invite_hash>', methods=['POST', 'OPTIONS'])
def accept_group_invite(invite_hash):
    # check for cookie
    # check group collection for group id
    # if exists, append group object to table
    # else throw error

    user = validate_cookie(request)
    responseWrapper = ResponseWrapper()
    response = any_response(request)

    if user != None:
        group_obj = groupDAO.get_group_by_hash(str(invite_hash))
        if group_obj != None:
            #  check if group is already part for the user
            group_exists = userDAO.does_group_exist(user.id,group_obj)
            print "group exists", group_exists
            append_group_result = None
            append_user_result = None

            if group_exists == False:
                append_group_result = groupDAO.append_user(group_obj, user.id)
                group_obj = groupDAO.get_group_by_id(group_obj.id)
                print " modified grp \n"
                print group_obj.__str__()
                append_user_result = userDAO.append_group(user.id,group_obj)
                
            else:
                responseWrapper.set_error(False)
                responseWrapper.set_data(["group already part of user"])

            # check for DB errors
            if append_user_result != False and append_group_result != False:
                responseWrapper.set_error(False)
                responseWrapper.set_data("")
            
            elif append_user_result == False:
                responseWrapper.set_error(True)
                responseWrapper.set_data(["error adding group to user"])
            
            else:
                responseWrapper.set_error(True)
                responseWrapper.set_data(["error adding user to group"])

        else:
            responseWrapper.set_error(True)
            responseWrapper.set_data(["No such group. Try again"])
    else:
        # TODO redirect to login page
        responseWrapper.set_error(True)
        responseWrapper.set_data(["User not found. Please login again"])
        response.status_code = 302

    response.data = json.dumps(responseWrapper, default=ResponseWrapper.__str__)
    response.mimetype = "application/json"
    return response


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
    print request.cookies
    
    cookies = request.cookies

    if 'session' in cookies:
        print "cookie : ",cookies['session']
        userid = sessionDAO.get_userid(cookies['session'])  # see if user is logged in
        print "user : ",userid
        if userid != None:
            user = userDAO.get_user_by_id(userid)
            print user.__str__()
            if user != None:
                return user

    return None

# CORS
def any_response(request):

  response = make_response()
  response.headers['Access-Control-Allow-Origin'] = "http://localhost:8000"
  # print request.headers
  if request.method == "OPTIONS" and 'Access-Control-Request-Headers' in request.headers:
      response.headers['Access-Control-Allow-Headers'] = request.headers['Access-Control-Request-Headers']
  response.headers['Access-Control-Allow-Credentials'] = "true"  
  response.headers['Access-Control-Allow-Methods'] = "GET, POST, DELETE, PUT, OPTIONS"

  return response

if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0',debug=True)

