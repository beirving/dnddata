from lib.base import BaseData


class Spell(BaseData):
    def edges(self) -> dict:
        return self._edges
