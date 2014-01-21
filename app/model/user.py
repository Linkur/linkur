__author__ = 'raghothams'

class User:
    # EMAIL
    # PASSWORD
    # NAME
    # GROUPS (COPY)

    def __init__(self, email=None, password=None, name=None, id=None):
        self.id = id
        self.email = email
        self.password = password
        self.name = name

    def __str__(self):

        return {
            '_id' : self.id,
            'email' : self.email,
            'password' : self.password,
            'name' : self.name,
        }

    def db_serializer(self):

        return {
            '_id' : self.id,
            'password' : self.password,
            'name' : self.name,
        }
