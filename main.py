from lib.base import BaseData


b = BaseData(cred_file_loc="creds/db.json")
b.name("bundle")
b.node("Bananas")
b.attributes("count", 3)
b.attributes("color", "yellow")
b.save()
