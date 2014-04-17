
import uuid

class Group:
    # ID
    # TITLE

    def __init__(self):
        self.id = None
        self.title = None

    def serialize(self):
        return {
            "id" : str(self.id),
            "title" : self.title
        }

