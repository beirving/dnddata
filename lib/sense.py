from lib.base import BaseData


class Sense(BaseData):
    def edges(self) -> list:
        return self._edges
