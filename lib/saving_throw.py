from lib.base import BaseData


class SavingThrow(BaseData):
    def edges(self) -> list:
        return self._edges

    @staticmethod
    def trim_extra(value: str):
        return value.replace("Saving Throw: ", "")
