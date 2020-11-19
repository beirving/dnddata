from lib.base import BaseData


class Alignment(BaseData):
    def edges(self) -> list:
        return self._edges

    @staticmethod
    def parse_alignment(string: str):
        morals = ["Good", "Neutral", "Evil"]
        socials = ["Lawful", "Neutral", "Chaotic"]
        string = string.title()
        print(string)
        return_value = []
        for social in socials:
            if string.find(social) > -1:
                return_value.append(social)
        for moral in morals:
            if string.find(moral) > -1:
                return_value.append(moral)

        return list(dict.fromkeys(return_value))