
import sys
sys.path.append("../")
from app.DAO.groupDAO import GroupDAO
from app.model.group import Group


def create_group():

    group = Group()
    data_mapper = GroupDAO()

    group.title = "3sb"

    data_mapper.add_group(group)

def change_group_name():

    group = Group()
    group.id = "03a56b57-01ba-5ddb-b4b1-9e19323d41b8"
    group.name = "2b1s"
    data_mapper = GroupDAO()

    data_mapper.change_group_name(group)

create_group()

