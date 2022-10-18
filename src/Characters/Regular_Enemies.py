from src.Characters.Bad_Character import BadCharacter
import src.Common_general_functionalities.common_strings as cs


class Orc(BadCharacter):

    @property
    def symbol(self):
        if self._undercover:
            return cs.unknown
        else:
            return cs.regular_enemy
