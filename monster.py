import requests
from lib.monster import Monster


base_url="http://dnd5eapi.co"
uri = "/api/monsters/lich"

request = requests.get(base_url+uri, verify=false)
data = request.json()

monster = Monster(cred_file_loc="creds/db.json")
monster.graph()
context = monster.graph().begin()

monster.create_or_update("Monster", data, context)

monster.handle_relations(context)
monster.graph().commit(context)
