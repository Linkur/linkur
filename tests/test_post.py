
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

    user_mapper = UserDAO()
    global user1
    user1 = user_mapper.add(user_model)
    assert user1

    user_model = User("tester2@test.com", "test123", "tester")

    user_mapper = UserDAO()
    global user2
    user2 = user_mapper.add(user_model)
    assert user2

def test_create_group():

    data_mapper = GroupDAO()

    user_mapper = UserDAO() 
    user = user_mapper.get_by_email("tester@test.com")

    group_name = "3sb"

    global group
    group = data_mapper.add(group_name, user.id)
    assert group

def test_join_group():
    group_mapper = GroupDAO()

    global group
    join_result = group_mapper.associate_user(user2, group)
    assert join_result

def test_create_post():

    global user1
    global group
    
    post_model = Post()
    post_model.title = "Test title"
    post_model.link = "http://www.google.com"
    post_model.group = group
    post_model.added_by = user1
    post_model.date = datetime.now()
    post_model.tags = ["lol1", "lol2"]

    post_mapper = PostDAO()
    result = post_mapper.create(post_model)

    global post
    post = result

    print result
    assert result

def test_get_all_posts_for_user():
    post_mapper = PostDAO()

    global user1
    global group
    print "group is ",group
    result = post_mapper.get_posts_for_group(group, user2)
    assert result

def test_get_post():

    post_mapper = PostDAO()
    global post
    global user2
    post_result = post_mapper.get(post, user2)

    assert post_result


def test_delete_post():

    global post

    user_mapper = UserDAO() 
    user = user_mapper.get_by_email("tester2@test.com")

    post_mapper = PostDAO()
    result = post_mapper.delete(post, user.id)

    assert result

def test_delete_group():

    data_mapper = GroupDAO()

    user_mapper = UserDAO() 
    user = user_mapper.get_by_email("tester@test.com")
    
    global group
    print "will remove association ",group
    assert data_mapper.remove_user_association(user.id, group)
    print "will delte ",group
    assert data_mapper.delete(group)


def test_delete_user():

    user_mapper = UserDAO()
    user = user_mapper.get_by_email("tester@test.com")
    assert user_mapper.delete(user.id)

    user = user_mapper.get_by_email("tester2@test.com")
    assert user_mapper.delete(user.id)

