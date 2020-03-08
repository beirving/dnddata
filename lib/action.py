from lib.base import BaseData


class Action(BaseData):
    def edges(self) -> dict:
        return self._edges
