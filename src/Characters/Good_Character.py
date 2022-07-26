from Character import Character


class GoodCharacter(Character):
    """
    We don't require a shield here, as some character can exist without having one.
    We need to build a tree for the weapons and shields, which this class can get the weapons from.
    Create Aids.
    """
    def __init__(self, life, undercover,  *items):
        if type(undercover) != bool:
            raise TypeError("Character's undercover value must be a boolean value.")
        weapon_serial, shield_serial, aids_serial = None, None, []
        for serial_number in items:
            if serial_number[:6] not in ["Weapon", "Shield"] and serial_number[:3] != "Aid":
                raise ValueError("The items a character can carry are either a Weapon, Shield, or an Aid.")
            if serial_number[:6] == "Weapon":
                if weapon_serial:
                    raise AttributeError("Character must have one weapon at most.")
                else:
                    weapon_serial = serial_number
            elif serial_number[:6] == "Shield":
                if shield_serial:
                    raise AttributeError("Character must have one shield at most.")
                else:
                    shield_serial = serial_number
            else:
                aids_serial.append(serial_number)

        if not weapon_serial:
            raise AttributeError("Character must have one weapon and at most one shield.")
        super().__init__(life)
        print("Life remaining: ", self._life)
        print("Weapons available: ", weapon_serial)
        print("Shields available: ", shield_serial)
        print("Aids available: ", aids_serial)
        #self._weapon = weapon
        #self._shield = shield
        self._undercover = undercover
        self._items = list(items)

    def items(self):                  # This kind of character must have a weapon, shield, and potentially more items.
        """List of items that character carries"""
        raise NotImplementedError

    def symbol(self):
        """The symbol on the printed maze that identifies the character"""
        raise NotImplementedError

    @property
    def attack(self):
        """Here we return the speed and strength of the weapon"""
        raise NotImplementedError

    @property
    def defend(self):
        """Here we return the speed and strength of the shield"""
        raise NotImplementedError

    @property
    def weapon_info(self):
        """This should return relevant information about the weapon."""
        raise NotImplementedError

    @property
    def shield_info(self):
        """This should return relevant information about the shield."""
        raise NotImplementedError

    @property
    def aids_info(self):
        """This should return relevant information about all the aids this character has."""
        raise NotImplementedError


if __name__ == '__main__':
    character = GoodCharacter(1200, True, "Weapon123", "Shield123")
    character.life_remain = 12
    print(character.life_remain)
    # del character.life_remain

