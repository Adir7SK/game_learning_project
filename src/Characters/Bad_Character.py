from Character import Character


class BadCharacter(Character):

    def __init__(self, max_life, life_remain, weapon, shield, *items):
        super().__init__(max_life, life_remain)
        self._weapon = weapon
        self._shield = shield

    def life_remain(self):
        """Getter method - returns life character currently has left"""
        super().life_remain

    def life_remain(self, damage):
        """Setter method - updates life after attack"""
        super().life_remain(damage)

    def items(self):                  # Perhaps this should not be implemented because an enemy gets a weapon in the beginning that won't change
        """List of items that character carries"""
        raise NotImplementedError

    def symbol(self):
        """The symbol on the printed maze that identifies the character"""
        raise NotImplementedError
