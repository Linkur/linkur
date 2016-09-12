__author__ = 'raghothams'

from bson.objectid import ObjectId
import datetime
from bson import ObjectId
# ID
# DATE
# TITLE
# LINK
# CATEGORY (categoryid) optional
# TAGS
# GROUP (groupid)
# ADDED BY USER (username)

class Post:

    def __init__(self):
        self.id = None
        self.date = None
        self.title = None
        self.link = None
        self.catgegory = None
        self.tags = None
        self.group = None
        self.added_by = None
        self.added_by_id = None

    # Use this to serialize the DB output
    def __str__(self):
        return {
        '_id' : str(self.id),
        'date' : str(self.date),
        'title' : self.title,
        'link' : self.link,
        'category' : self.catgegory,
        'tags' : self.tags,
        'group' : str(self.group),
        'added_by' : self.added_by,
        'added_by_id' : self.added_by_id
        }


    # Use this to serialize the DB input
    def db_serializer(self):
        return {
        'date' : datetime.datetime.utcnow(),
        'title' : self.title,
        'link' : self.link,
        'category' : self.catgegory,
        'tags' : self.tags,
        'group' : ObjectId(self.group),
        'added_by' : self.added_by,
        'added_by_id' : self.added_by_id
        }

    def tostring(self):
        return str({
        '_id' : str(self.id),
        'date' : str(self.date),
        'title' : self.title,
        'link' : self.link,
        'category' : self.catgegory,
        'tags' : self.tags,
        'group' : str(self.group),
        'added_by' : self.added_by,
        'added_by_id' : self.added_by_id
        })
