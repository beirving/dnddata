from lib.base import BaseData


class Language(BaseData):
    def edges(self) -> list:
        return self._edges

    @staticmethod
    def parse_lang(string: str) -> list:
        # remove annoying "plus up to x other languages"
        if string.find('plus'):
            split = string.split('plus')
            string = split[0]
        string = string.title()
        if len(string) == 0:
            return []
        if string.find(",") > -1:
            split = string.split(',')
            return split
        else:
            return [string]
