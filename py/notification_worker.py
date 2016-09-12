import ast
import os
import zmq
from pymongo import MongoClient
from bson import ObjectId
from urkin.DAO.groupDAO import GroupDAO
from urkin.redis.redis_queue import RedisQueueHelper

class NotificationBuilder:

    def __init__(self):
        self.mongoclient = MongoClient("localhost", 27017)
        self.db = self.mongoclient.test
        #db.authenticate("user", "password")
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PULL)
        self.socket.connect("tcp://127.0.0.1:5559")
        self.groups = self.db.groups
        self.redis_helper = RedisQueueHelper()

    def listen(self):

        while(True):
            post = self.socket.recv()
            print(post)
            post_dict = ast.literal_eval(post)

            self.build_notification(post_dict)

    def build_notification(self, post):
        groupDAO = GroupDAO(self.db)
        group = groupDAO.get_group_by_id(post["group"])

        for user in group.users:
            if user != post["added_by_id"]:
                self.redis_helper.push_notification(user, str(post))
        print("notification push to redis success")

if __name__ == "__main__":
    print(os.getcwd())
    q = NotificationBuilder()
    q.listen()
    #p = {'category': None, 'link': u'ada', 'added_by_id': u'tester@test.com', 'title': u'asas', 'date': 'None', 'group': '57d6d5ac0c8a501e5a5ca813', '_id': 'None', 'tags': [u'as']}
    #q.build_notification(p)
