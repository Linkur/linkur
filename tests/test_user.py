
# file to add tests for userDAO.py
import uuid
import psycopg2.extras
from DAO.userDAO import UserDAO
from model.user import User
import conf

def test_nose():
    assert True

# test to create a user
def user_create():

    try:

        user = User("tester@test.com", "test123", "tester")

        user_mapper = UserDAO()
        user_mapper.add_user(user)

    except Exception as e:

        assert False

    assert True

def change_password():

    try:

        user_mapper = UserDAO()
        uid = uuid.UUID("84319fd4-c820-5289-ab32-dad7e25d6ad9")
        uid = psycopg2.extras.UUID_adapter(uid);
        user_mapper.change_password(uid, "test123", "testing123")

    except Exception as e:

        assert False

    assert True

