
from app.DAO.groupDAO import GroupDAO
from app.DAO.userDAO import UserDAO
from app.model.user import User

global group
group = None

# test to create a user
def test_user_create():

    user = User("tester@test.com", "test123", "tester")

    user_mapper = UserDAO("LOL")
    assert user_mapper.add(user)

def test_create_group():

    data_mapper = GroupDAO()

    user_mapper = UserDAO("LOL") 
    user = user_mapper.get("tester@test.com")

    group_name = "3sb"

    global group
    group = data_mapper.add(group_name, user.id)
    assert group


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

