from lib.base import BaseData


class DamageType(BaseData):
    def edges(self) -> list:
        return self._edges

    @staticmethod
    def parse_combine_damage(value: str) -> tuple:
        value = value.replace("and", "").replace(" ", "")
        split = value.split('from')
        return split[0].split(","), split[1]

