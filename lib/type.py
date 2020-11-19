from lib.base import BaseData


class Type(BaseData):
    def edges(self) -> list:
        return self._edges
