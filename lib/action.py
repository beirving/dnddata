from lib.base import BaseData


class Action(BaseData):
    def edges(self) -> list:
        return self._edges
