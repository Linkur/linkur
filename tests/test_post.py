
# file to add tests for userDAO.py
import uuid
import psycopg2.extras
from datetime import datetime

import sys
sys.path.append("../")
from app.DAO.userDAO import UserDAO
from app.DAO.postDAO import PostDAO
from app.model.user import User
from app.model.post import Post


def test_nose():
    assert True, "Nose success"

def test_create_post():

    user_mapper = UserDAO()
    post_mapper = PostDAO()
    user_id = user_mapper.get_user_id("dev@dev.com")
    print "user_id ",user_id
    group_id = "48c9a20f-1c5f-5759-8669-2ffb1691a47f"

    if user_id and group_id:

        post = Post()
        post.title = "test1"
        post.date = datetime.now()
        post.link = "http://google.com"
        post.group = group_id
        post.added_by = user_id
        post.tags = ["ping", "pong"]
        uid = uuid.UUID("84319fd4-c820-5289-ab32-dad7e25d6ad9")
        uid = psycopg2.extras.UUID_adapter(uid);
        post.id = uid

        post_mapper.create_post(post)
    
    else:
        print "error no user / group"

test_create_post()

