__author__ = 'raghothams'

from urkin.model.user import User
from urkin.model.group import Group
from urkin.DAO.groupDAO import GroupDAO
from bson import ObjectId
# import hmac
import pymongo
import hashlib
import random
import string

class UserDAO:

    def __init__(self, database):
        self.db = database
        self.user_collection = self.db.users
        # self.SECRET = 'thisissuperdupersecret'

    def make_salt(self):
        salt = ""
        for i in range(5):
            salt = salt + random.choice(string.ascii_letters)
        return salt

    def make_pw_hash(self, pw, salt=None):
        if salt == None:
            salt = self.make_salt()
        return hashlib.sha256(pw + salt).hexdigest()+","+salt

    def validate_login(self, uname, pw):
        return_data = {"error":None,"data":None}
        user = None
        try:
            collection = self.user_collection
            user = collection.find_one({"_id":uname})

        except Exception as inst:
            print "error finding user"
            return_data["error"]=True
            return_data["data"]=["error finding user"]
            return return_data

        if user is None:
            print "User not in database"
            return_data["error"]=True
            return_data["data"]=["User not in database"]
            return return_data

        password = user["password"]
        salt = password.split(',')[1]

        # Check if the user password matches
        if password != self.make_pw_hash(pw, salt):
            print "user password is not a match"
            return_data["error"]=True
            return_data["data"]=["user password is not a match"]
            return return_data

        # User password matches. Return user
        return_data["error"]=False
        return_data["data"]=user
        return return_data


    def add_user(self, modelled_user):

        # convert password to hash before storing it in DB
        password_hash = self.make_pw_hash(modelled_user.password)

        user = {
                    '_id' : modelled_user.id,
                    'password' : password_hash,
                    'name' : modelled_user.name,
                    'groups' : modelled_user.groups
                }

        try:
            collection = self.user_collection
            result = collection.insert(user)
            print "insert result :"+result

        except Exception as inst:
            print inst
            return False

        return True

    def get_user_info(self, uname):

        user = self.get_user_by_id(uname)
        user.password = None
        user.id = None
        groups_list = []
        if user != None:
            #  get the groups data
            for group in user.groups:
                try:
                    groupDAO = GroupDAO(self.db)
                    group_obj = groupDAO.get_group_by_id(str(group['_id']))

                    group_data = {
                        '_id': str(group_obj.id),
                        'name': group_obj.name,
                        'hash': group_obj.hash
                    }
                    groups_list.append(group_data)

                except Exception as inst:
                    print "error readin group data"
                    print inst
                    return None

            user.groups = groups_list
            return user

        else:
            print "user not in DB."
            return "Cannot find User"


    def get_user_by_id(self, uname):
        user = None
        try:
            collection = self.user_collection
            user_record = collection.find_one({"_id":uname})

            user = User(user_record['_id'], user_record['password'], user_record['name'])
            user.groups = user_record['groups']

        except Exception as inst:
            print "error finding user"
            print inst

        if user is None:
            print "User not in database"
            return None
        else:
            return user

    def get_groups(self, uname):
        # get all groups for this user
        group = None
        user_groups = None
        try:
            collection = self.user_collection
            user_groups = collection.find_one({'_id':uname},{"groups":True})
        except Exception as inst:
            print "error reading groups"
            print inst

        if user_groups != None:

            group_cursor = user_groups["groups"]
            groups = []

            for item in group_cursor:
                print item
                group = Group()
                group.id = str(item["_id"])
                group.name = item["name"]
                group.hash = item["hash"]

                groups.append(group)

            return groups
        else:
            return None

    #  append group to user
    def append_group(self, uname, group_obj):
        # append this group to the groups array of the user document
        collection = self.user_collection
        group = group_obj.__str__()
        try:
            result = collection.update({"_id":uname},{"$push":{"groups":group}})
        except Exception as inst:
            print "error updating DB"
            print inst
            return False

        return True

    def does_group_exist(self, uname, group_obj):
        collection = self.user_collection
        result = None
        print group_obj.id
        try:
            result = collection.find_one({"_id":uname, "groups._id":group_obj.id})
        except Exception as inst:
            print "error updating DB"
            print inst
        if  result != None:
            # do something
            print(result['_id'])
            return True
        else:
            return False

    #  remove group to user
    def remove_group(self, uname, group_obj):
        # append this group to the groups array of the user document
        collection = self.user_collection
        # group = group_obj.__str__()
        try:
            result = collection.update({"_id":uname},
                {"$pull":{"groups":{"_id":ObjectId(group_obj.id)}}} )

        except Exception as inst:
            print "error updating user DB - removing group from user"
            print inst
            return False

        return True

    # change_user_password
    def change_password(self, uname, password, new_password):

        # call validate login & validate user
        # on success change password

        validation_result = self.validate_login(uname, password)

        # check if user is validated
        if validation_result != None and validation_result["error"] == False:

            # convert the new password to hash before updating DB
            new_password_hash = self.make_pw_hash(new_password)

            # Data to be updated, for query
            update_data = {
                    'password' : new_password_hash,
                }

            collection = self.user_collection
            update_result = collection.update({
                                    "_id" : uname
                                },
                                {"$set" : update_data},
                                safe=True
                            )

            return update_result

        else:
            print "user no match"
            return None
