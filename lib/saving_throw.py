from lib.base import BaseData


class SavingThrow(BaseData):
    def edges(self) -> dict:
        return self._edges

    @staticmethod
    def trim_extra(value: str):
        return value.replace("Saving Throw: ", "")
