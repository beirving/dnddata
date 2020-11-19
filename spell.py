import requests
from lib.spell import Spell

base_url="http://dnd5eapi.co"
uri = "/api/spells"

request = requests.get(base_url+uri)
data = request.json()

for spell in data['results']:
    request = requests.get(base_url + spell['url'])
    spell_data = request.json()
    spell_obj = Spell(cred_file_loc="creds/db.json")
    spell_obj.graph()
    context = spell_obj.graph().begin()

    spell_obj.create_or_update("Spell", spell_data, context)

    spell_obj.handle_relations(context)
    context.commit()
