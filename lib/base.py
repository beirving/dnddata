from neo4j import GraphDatabase, Driver
import json
import os


class BaseData(object):
    def __init__(self, cred_file_loc: str) -> None:
        self._name = None
        self._node = None
        self._attributes = {}
        self._edges = {}
        self._driver = None
        if os.path.isfile(cred_file_loc):
            self._cred_loc = cred_file_loc
        else:
            raise FileNotFoundError

    def create_connection(self):
        config = json.loads(open(self._cred_loc).read())
        self._driver = GraphDatabase.driver(
            config['url'],
            auth=(config['username'], config['password'])
        )
        del config

    def close(self) -> None:
        self._driver.close()

    def name(self, value: str = None) -> str:
        if value is not None:
            self._name = value
        return self._name

    def node(self, value: str = None) -> str:
        if value is not None:
            self._node = value
        return self._node

    def attributes(self, key: str = None, value: str = None) -> dict:
        if key is not None:
            self._attributes[key] = value
        return self._attributes

    def edges(self, key: str = None, value=None) -> dict:
        if key is not None:
            self._edges[key] = value
        return self._edges

    def output_attributes(self) -> str:
        output = ''
        if len(self._attributes) > 0:
            for key, value in self._attributes.items():
                if type(value) is str:
                    value = f"'{value}'"
                if len(output) == 0:
                    output = f"{key}:{value}"
                output = output + f", {key}:{value}"
        return output

    def search_exists(self):
        self.create_connection()
        query = f"MATCH (n:{self.node()} {{name:'{self.name()}'}}) RETURN id(n)"
        with self._driver.session() as session:
            result = session.write_transaction(self._run_and_return, query)
            self.close()
            if result.single() is None:
                return False
            return True

    def create(self) -> str:
        output = f"CREATE (n:{self.node()} {{name:'{self.name()}'}}) "
        output = output + "SET n += {{{}}} ".format(self.output_attributes())
        output = output + "RETURN id(n)"
        return output

    def update(self) -> str:
        output = f"MATCH (n:{self.node()} {{name:'{self.name()}'}}) "
        output = output + "SET n += {{{}}} ".format(self.output_attributes())
        output = output + "RETURN id(n)"
        return output

    def save(self) -> int:
        if self.search_exists():
            query = self.update()
        else:
            query = self.create()

        self.create_connection()
        with self._driver.session() as session:
            result = session.write_transaction(self._run_and_return, query)
            node = result.single()
            self.close()
            print(type(node))
            print(node)

    @staticmethod
    def _run_and_return(tx, query):
        return tx.run(query)
