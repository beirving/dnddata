from lib.base import BaseData
from typing import Union


class Component(BaseData):
    def edges(self) -> list:
        return self._edges

    @staticmethod
    def letter_to_word(letter: str) -> Union[str,bool]:
        dictionary = {
            "V": "Verbal",
            "S": "Somatic",
            "M": "Material",
            "F": "Focus",
            "DF": "Divine Focus"
        }
        if letter.upper() in dictionary:
            return dictionary[letter.upper()]
        else:
            print(letter)
            return False
