from lib.base import BaseData


class Type(BaseData):
    def edges(self) -> dict:
        return self._edges
