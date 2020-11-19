from lib.base import BaseData


class SubClass(BaseData):
    def edges(self) -> list:
        return self._edges
