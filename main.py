from lib.base import BaseData
from py2neo import Node, Relationship

base = BaseData(cred_file_loc="creds/db.json")

context = base.graph().begin()

a = Node("Person", name="Alice")
check_exists = base.get_node(a)
if check_exists is False:
    context.create(a)
else:
    a = check_exists
    context.merge(a)
    a['gender'] = "Female"
    context.push(a)

b = Node("Person", name="Bob")
check_exists = base.get_node(b)
if check_exists is False:
    context.create(b)
else:
    b = check_exists
    context.merge(b)
    a['gender'] = "Male"
    context.push(b)

ab = Relationship(a, "WORKED_WITH", b)
ab["years"] = 5
ab["test"] = "test"
if base.graph().exists(ab) is True:
    context.merge(ab)
else:
    context.create(ab)

context.commit()

