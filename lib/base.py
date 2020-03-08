from py2neo import (
    Graph,
    NodeMatcher,
    RelationshipMatcher,
    Node,
    Relationship,
    Transaction
)
from typing import Union
import json
import os


class BaseData(object):
    def __init__(self, cred_file_loc: str) -> None:
        self._node = None
        self._edges = {}
        self._relations = {}
        self._graph = None
        if os.path.isfile(cred_file_loc):
            self._cred_loc = cred_file_loc
        else:
            raise FileNotFoundError

    def graph(self):
        if self._graph is None:
            config = json.loads(open(self._cred_loc).read())
            self._graph = Graph(
                host=config['host'],
                scheme=config['scheme'],
                port=config['port'],
                user=config['username'],
                password=config['password']
            )
            del config
        return self._graph

    def get_node(self, node: Node) -> Union[Node,bool]:
        matcher = NodeMatcher(self.graph())
        name = f"{node['name']}"
        label = f"{node.labels}".replace(":", "")
        result = matcher.match(label, name=name).first()
        if result is None:
            return False
        else:
            return result

    def create_node(self, label: str = None, name: str = None) -> Node:
        if self._node is None:
            self._node = Node(label, name=name)
        return self._node

    def node(self, node: Node = None) -> Node:
        if node is not None:
            self._node = node
        return self._node

    def relations(self):
        return self._relations

    def edges(self) -> dict:
        return self._edges

    def assign_attributes(self, data: dict) -> None:
        for key, value in data.items():
            if key in self.edges():
                self._relations[key] = value
            else:
                self._node[key] = value

    def create_or_update(self, label: str, data: dict, context: Transaction):
        self.create_node(label=label, name=data['name'])

        check_node = self.get_node(self.node())
        exits = False
        if type(check_node) is Node:
            exits = True
            self.node(check_node)

        self.assign_attributes(data)

        if exits is False:
            context.create(self.node())
            print(f"Created {label}")
        else:
            context.push(self.node())
            print(f"Updated {label}")

    def handle_relations(self, context: Transaction):
        pass

    def create_or_merge_relationship(self, relation: Relationship, context: Transaction):
        if self.graph().exists(relation) is True:
            context.merge(relation)
        else:
            context.create(relation)