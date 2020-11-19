from lib.base import BaseData


class Proficiency(BaseData):
    def edges(self) -> list:
        return self._edges

    @staticmethod
    def trim_extra(value: str):
        return value.replace("Skill: ", "")
