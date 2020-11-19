from lib import (
    base,
    school as school,
    classes as classes,
    subclass as subclasses,
    component as component
)


class SpellCasting(base.BaseData):
    def edges(self) -> list:
        return self._edges

