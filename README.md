# dnddata
load data from dnd5eapi.co into Neo4j 


requires cred/db.json file in root directory.

db.json contents should be:
{
  "url": "bolt://localhost:7687",
  "host": "localhost",
  "scheme": "bolt",
  "port": "7687",
  "username": "username",
  "password": "password"
}
