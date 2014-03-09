
import uuid

class Group:
    # ID
    # TITLE

    def __init__(self):
        self.id = None
        self.title = None

    def __str__(self):
        return {
            "id" : str(self.id),
            "title" : self.title
        }

    def db_serializer(self):
        return {
            "title" : self.title
        }

