from lib import (
    base,
    action as action,
    alignment as alignment,
    condition as condition,
    damage_type as damage_type,
    language as language,
    legendary_action as legendary_action,
    proficiency as proficiency,
    saving_throw as saving_throw,
    sense as sense,
    size as size,
    special_ability as special_ability,
    speed as speed,
    spell as spell,
    subtype as subtype,
    type as type
)
from py2neo import (
    Graph,
    NodeMatcher,
    RelationshipMatcher,
    Node,
    Relationship,
    Transaction
)


class Monster(base.BaseData):

    def edges(self) -> list:
        self._edges = [
            "actions",
            "alignment",
            "condition_immunities",
            "damage_immunities",
            "damage_resistances",
            "damage_vulnerabilities",
            "languages",
            "legendary_actions",
            "proficiencies",
            "senses",
            "size",
            "special_abilities",
            "speed",
            "spellcasting",
            "subtype",
            "type"
        ]
        return self._edges

    def handle_relations(self, context: Transaction):
        if "actions" in self._relations:
            self.actions(context)
        if "alignment" in self._relations:
            self.alignment(context)
        if "condition_immunities" in self._relations:
            self.conditions(context)
        if "damage_immunities" in self._relations:
            self.damage("IMMUNITY", self._relations['damage_immunities'], context)
        if "damage_resistances" in self._edges:
            self.damage("RESISTANCE", self._relations['damage_resistances'], context)
        if "damage_vulnerabilities" in self._edges:
            self.damage("VULNERABILITY",self._relations['damage_vulnerabilities'],  context)
        if "languages" in self._relations:
            self.languages(context)
        if "legendary_actions" in self._relations:
            self.legendary_actions(context)
        if "proficiencies" in self._relations:
            self.proficiencies(context)
        if "senses" in self._relations:
            self.senses(context)
        if "size" in self._relations:
            self.size(context)
        if "speed" in self._relations:
            self.speed(context)
        if "spellcasting" in self._relations:
            self.spellcasting(context)
        if "subtype" in self._relations:
            self.subtype(context)
        if "type" in self._relations:
            self.type(context)

    def actions(self, context: Transaction):
        pass

    def alignment(self, context: Transaction):
        node_obj = alignment.Alignment(self._cred_loc)
        alignments = alignment.Alignment.parse_alignment(self._relations['alignment'])
        for ali in alignments:
            node_obj.create_or_update("Alignment", {"name": ali}, context)
            relation = Relationship(self.node(), f"ALIGNMENT", node_obj.node())
            self.create_or_merge_relationship(relation, context)

    def conditions(self, context: Transaction):
        for condition_item in self._relations['condition_immunities']:
            node_obj = condition.Condtion(self._cred_loc)
            node_obj.create_or_update("Condition", {"name": condition_item['name']}, context)
            relation = Relationship(self.node(), f"IMMUNITY", node_obj.node())
            self.create_or_merge_relationship(relation, context)

    def damage(self, relation_name: str, data: list, context: Transaction, qualifier: str = None):
        if len(data) == 0:
            pass
        for value in data:
            if value.find(',') > -1:
                value = damage_type.DamageType.parse_combine_damage(value)
                self.damage(relation_name, value[0], context, value[1])
            else:
                node_obj = damage_type.DamageType(self._cred_loc)
                node_obj.create_or_update("Damage", {"name": value.title()}, context)
                relation = Relationship(self.node(), relation_name, node_obj.node())
                if qualifier is not None:
                    relation['from'] = qualifier
                self.create_or_merge_relationship(relation, context)

    def languages(self, context: Transaction):
        langs = self._relations['languages']
        langs = language.Language.parse_lang(langs)
        if len(langs) > 0:
            for lang in langs:
                node_obj = language.Language(self._cred_loc)
                node_obj.create_or_update("Language", {"name": lang}, context)
                relation = Relationship(self.node(), f"CAN_SPEAK", node_obj.node())
                self.create_or_merge_relationship(relation, context)

    def legendary_actions(self, context: Transaction):
        pass

    def proficiencies(self, context: Transaction):
        for item in self._relations['proficiencies']:
            if item['name'].find("Saving") > -1:
                node_obj = saving_throw.SavingThrow(self._cred_loc)
                format_name = node_obj.trim_extra(item['name'])
                node_obj.create_or_update("Saving Throw", {"name": format_name}, context)
                relation = Relationship(self.node(), f"HAS_SAVING_THROW", node_obj.node())
            else:
                node_obj = proficiency.Proficiency(self._cred_loc)
                format_name = node_obj.trim_extra(item['name'])
                node_obj.create_or_update("Proficiency", {"name": format_name}, context)
                relation = Relationship(self.node(), f"HAS_PROFICIENCY", node_obj.node())
            relation['value'] = item['value']
            self.create_or_merge_relationship(relation, context)

    def senses(self, context: Transaction):
        for name, value in self._relations['senses'].items():
            node_obj = speed.Speed(self._cred_loc)
            format_name = name.replace("_", " ").title()
            node_obj.create_or_update("Sense", {"name": format_name}, context)
            relation = Relationship(self.node(), f"HAS_SENSE", node_obj.node())
            relation['value'] = value
            self.create_or_merge_relationship(relation, context)

    def size(self, context: Transaction):
        node_obj = size.Size(self._cred_loc)
        node_obj.create_or_update("Size", {"name": f"{self._relations['size']}".title()}, context)
        relation = Relationship(self.node(), f"SIZE", node_obj.node())
        self.create_or_merge_relationship(relation, context)

    def speed(self, context: Transaction):
        for name, value in self._relations['speed'].items():
            node_obj = speed.Speed(self._cred_loc)
            node_obj.create_or_update("Speed", {"name": name.title()}, context)
            relation = Relationship(self.node(), f"SPEED", node_obj.node())
            relation['speed'] = value
            self.create_or_merge_relationship(relation, context)

    def spellcasting(self, context: Transaction):
        pass

    def subtype(self, context: Transaction):
        pass

    def type(self, context: Transaction):
        pass

