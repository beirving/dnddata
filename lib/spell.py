from lib import (
    base,
    school as school,
    classes as classes,
    subclass as subclasses,
    component as component
)
from py2neo import (
    Transaction,
    Relationship
)


class Spell(base.BaseData):
    def edges(self) -> list:
        self._edges = [
            "school",
            "classes",
            "subclasses",
            "components",
            "_id",
            "index",
            "url"
        ]
        return self._edges

    def handle_relations(self, context: Transaction):
        if "school" in self._relations:
            self.school(context)
        if "classes" in self._relations:
            self.classes(context)
        if "subclasses" in self._relations:
            self.subclasses(context)
        if "components" in self._relations:
            self.components(context)

    def school(self, context: Transaction):
        node_obj = school.School(self._cred_loc)
        node_obj.create_or_update("School", {"name": f"{self._relations['school']['name']}"}, context)
        relation = Relationship(self.node(), f"SCHOOL", node_obj.node())
        self.create_or_merge_relationship(relation, context)

    def classes(self, context: Transaction):
        for game_class in self._relations['classes']:
            node_obj = classes.Classes(self._cred_loc)
            node_obj.create_or_update("Class", {"name": game_class['name']}, context)
            relation = Relationship(self.node(), f"CASTABLE_BY", node_obj.node())
            self.create_or_merge_relationship(relation, context)

    def subclasses(self, context: Transaction):
        for game_subclass in self._relations['subclasses']:
            node_obj = subclasses.SubClass(self._cred_loc)
            node_obj.create_or_update("SubClass", {"name": game_subclass['name']}, context)
            relation = Relationship(self.node(), f"CASTABLE_BY", node_obj.node())
            self.create_or_merge_relationship(relation, context)

    def components(self, context: Transaction):
        for comp in self._relations['components']:
            node_obj = component.Component(self._cred_loc)
            name = component.Component.letter_to_word(comp)
            if name is not False:
                node_obj.create_or_update("Component", {"name": name}, context)
                relation = Relationship(self.node(), f"REQUIRED", node_obj.node())
                self.create_or_merge_relationship(relation, context)
