
# file to add tests for userDAO.py
from DAO.userDAO import UserDAO
from model.user import User
import conf

# test to create a user
def user_create():

    user = User("dev@dev.com", "dev123", "dev")

    user_mapper = UserDAO()
    user_mapper.add_user(user)

user_create()
