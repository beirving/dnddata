from lib.base import BaseData


class SubType(BaseData):
    def edges(self) -> dict:
        return self._edges
