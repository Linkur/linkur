
from app.DAO.groupDAO import GroupDAO
from app.DAO.userDAO import UserDAO
from app.model.user import User

global groupid
group = None

# test to create a user
def test_user_create():

    user = User("tester@test.com", "test123", "tester")

    user_mapper = UserDAO()
    assert user_mapper.add(user)

def test_create_group():

    data_mapper = GroupDAO()

    user_mapper = UserDAO() 
    user = user_mapper.get_by_email("tester@test.com")

    group_name = "3sb"
    group = data_mapper.add(group_name, user.id)
    assert group

    group_name = "IC"
    global groupid
    group = data_mapper.add(group_name, user.id)
    groupid = group
    assert group

def test_get_all_for_user():

    data_mapper = GroupDAO()

    user_mapper = UserDAO() 
    user = user_mapper.get_by_email("tester@test.com")
    
    print user.id
    groups = data_mapper.get_all(user.id)
    print groups
    assert groups

def test_get():

    data_mapper = GroupDAO()

    user_mapper = UserDAO() 
    user = user_mapper.get_by_email("tester@test.com")
    
    global groupid
    group = data_mapper.get(groupid)
    assert group

def test_delete_group():

    data_mapper = GroupDAO()

    user_mapper = UserDAO() 
    user = user_mapper.get_by_email("tester@test.com")
    
    groups = data_mapper.get_all(user.id)

    for group in groups:
        print "will remove group association "
        assert data_mapper.remove_user_association(user.id, group['id'])
        print "will delte group "
        assert data_mapper.delete(group['id'])

    print "Done deleting groups"


def test_delete_user():

    user_mapper = UserDAO()
    user = user_mapper.get_by_email("tester@test.com")
    assert user_mapper.delete(user.id)

