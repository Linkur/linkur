
# file to add tests for userDAO.py
import uuid
import psycopg2.extras
from DAO.userDAO import UserDAO
from model.user import User
import conf

# test to create a user
def user_create():

    user = User("tester@test.com", "test123", "tester")

    user_mapper = UserDAO()
    user_mapper.add_user(user)

def change_password():

    user_mapper = UserDAO()
    uid = uuid.UUID("84319fd4-c820-5289-ab32-dad7e25d6ad9")
    uid = psycopg2.extras.UUID_adapter(uid);
    user_mapper.change_password(uid, "test123", "testing123")

change_password()
