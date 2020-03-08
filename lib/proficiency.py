from lib.base import BaseData


class Proficiency(BaseData):
    def edges(self) -> dict:
        return self._edges

    @staticmethod
    def trim_extra(value: str):
        return value.replace("Skill: ", "")
