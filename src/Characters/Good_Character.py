from Character import Character


class GoodCharacter(Character):

    def __init__(self, max_life, life_remain, weapon, shield, *items):
        super().__init__(max_life, life_remain)
        self._weapon = weapon
        self._shield = shield
        self._items = list(items)

    def items(self):                  # This kind of character must have a weapon, shield, and potentially a few items.
        """List of items that character carries"""
        raise NotImplementedError

    def symbol(self):
        """The symbol on the printed maze that identifies the character"""
        raise NotImplementedError
