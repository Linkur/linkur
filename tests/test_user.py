
# file to add tests for userDAO.py
import uuid
import psycopg2.extras

import sys
sys.path.append("../")
from app.DAO.userDAO import UserDAO
from app.model.user import User


def test_nose():
    assert True, "Nose success"

# test to create a user
def test_user_create():

    user = User("tester@test.com", "test123", "tester")

    user_mapper = UserDAO()
    assert user_mapper.add_user(user)


def test_change_password():

    user_mapper = UserDAO()
    uid = uuid.UUID("84319fd4-c820-5289-ab32-dad7e25d6ad9")
    uid = psycopg2.extras.UUID_adapter(uid);
    assert user_mapper.change_password(uid, "test123", "testing123")

