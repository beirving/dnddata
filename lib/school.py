from lib.base import BaseData


class School(BaseData):
    def edges(self) -> dict:
        return self._edges
