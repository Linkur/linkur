
# file to add tests for userDAO.py
import uuid
import psycopg2.extras
from datetime import datetime

import sys
sys.path.append("../")
from app.DAO.userDAO import UserDAO
from app.DAO.postDAO import PostDAO
from app.DAO.groupDAO import GroupDAO
from app.model.user import User
from app.model.post import Post
from app.model.group import Group

global group
group = None

global user
user = None

def test_nose():
    assert True, "Nose success"

# test to create a user
def test_user_create():

    user_model = User("tester@test.com", "test123", "tester")

    user_mapper = UserDAO("LOL")
    global user
    user = user_mapper.add(user_model)
    assert user


def test_create_group():

    data_mapper = GroupDAO()

    user_mapper = UserDAO("LOL") 
    user = user_mapper.get("tester@test.com")

    group_name = "3sb"

    global group
    group = data_mapper.add(group_name, user.id)
    assert group

def test_create_post():

    global user
    global group
    
    post_model = Post()
    post_model.title = "Test title"
    post_model.link = "http://www.google.com"
    post_model.group = group
    post_model.added_by = user
    post_model.date = datetime.now()
    post_model.tags = ["lol1", "lol2"]

    post_mapper = PostDAO()
    result = post_mapper.create(post_model)

    global post
    post = result

    print result
    assert result

def test_delete_post():

    global post

    post_mapper = PostDAO()
    result = post_mapper.delete(post)

    assert result

def test_delete_group():

    data_mapper = GroupDAO()

    user_mapper = UserDAO("LOL") 
    user = user_mapper.get("tester@test.com")
    
    global group
    print "will remove association ",group
    assert data_mapper.remove_user_association(user.id, group)
    print "will delte ",group
    assert data_mapper.delete(group)


def test_delete_user():

    user_mapper = UserDAO("LOL")
    user = user_mapper.get("tester@test.com")
    assert user_mapper.delete(user.id)

