from lib.base import BaseData


class SubType(BaseData):
    def edges(self) -> list:
        return self._edges
