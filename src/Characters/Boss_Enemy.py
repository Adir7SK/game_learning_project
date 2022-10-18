from src.Characters.Bad_Character import BadCharacter
import src.Common_general_functionalities.common_strings as cs


class Boss(BadCharacter):

    def __init__(self, life, weapon, shield):
        super().__init__(life, False, weapon, shield)

    @property
    def symbol(self):
        return cs.boss
