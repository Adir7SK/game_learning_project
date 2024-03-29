from src.Armor.Shield import Shield
from src.Armor.Weapon import Weapon
from src.Characters.Character import Character
from src.Data_Loading.Data_Placement import GameDetailsData
import src.Common_general_functionalities.common_strings as cs


class BadCharacter(Character):
    """
        This class defines a bad character (enemy) in the game. This can either be an undercover enemy or declared
        enemy (can be simple enemy like troll, oger, or a boss).

        Upon initialization there is a check of the input data. There's a validation that the character will carry
        exactly one weapon and one shield, and nothing else.

        If there is no weapon or shield at initialization, the character will automatically have his hand as weapon
        and shield. There are getters, setters and (anti) deleter for weapon, shield and undercover.

        For the practical implementation, there is a method that should return the symbol of the current character on
        the map. There is also a method for attack and defend. Both return the speed and strength of the weapon/shield
        the character possesses. These will later determine how much damage they cause to the opponent and how much they
        reduce an attack from the opponent.
        """

    def __init__(self, life, undercover, *items):
        if type(undercover) != bool:
            raise TypeError("Character's undercover value must be a boolean value.")
        self._weapon, self._shield = None, None
        for item in items:
            if not isinstance(item, (Shield, Weapon)):
                raise AttributeError("Attributes after undercover must be either Weapon, or Shield type.")
            serial_number = item.serial_number()
            if serial_number[:6] not in [cs.weapon, cs.shield]:
                raise AttributeError("The items a character can carry are either a Weapon or Shield.")
            if serial_number[:6] == cs.weapon:
                if self._weapon:
                    raise AttributeError("Character must have one weapon at most.")
                else:
                    self._weapon = item
            elif serial_number[:6] == cs.shield:
                if self._shield:
                    raise AttributeError("Character must have one shield at most.")
                else:
                    self._shield = item

        if not self._weapon:
            weapons = (GameDetailsData().get_armor_data())[cs.weapons]
            i = 1
            while not weapons.search(i):
                i += 1
            self._weapon = weapons.search(i)
        if not self._shield:
            shields = (GameDetailsData().get_armor_data())[cs.shields]
            i = 1
            while not shields.search(i):
                i += 1
            self._shield = shields.search(i)

        super().__init__(life)
        self._undercover = undercover

    @property
    def symbol(self):
        """The symbol on the printed maze that identifies the character"""
        raise NotImplementedError

    def items(self):
        return None

    @property
    def undercover(self):
        return self._undercover

    @undercover.setter
    def undercover(self, value):
        if isinstance(value, bool):
            self._undercover = value
        else:
            raise TypeError("The undercover value must be boolean.")

    @property
    def weapon(self):
        return self._weapon

    @weapon.setter
    def weapon(self, serial_number):
        if serial_number[:6] != cs.weapon:
            raise ValueError("Invalid weapon serial number. Valid example: Weapon460.")
        weapons = (GameDetailsData().get_armor_data())[cs.weapons]
        if weapons.search(int(serial_number[6:])):
            self._weapon = weapons.search(int(serial_number[6:]))
        else:
            raise ValueError("This serial number does not exist.")

    @weapon.deleter
    def weapon(self):
        raise AttributeError("Character must have a weapon, and you are trying to delete it.")

    @property
    def shield(self):
        return self._shield

    @shield.setter
    def shield(self, serial_number):
        if serial_number[:6] != cs.shield:
            raise ValueError("Invalid shield serial number. Valid example: Shield460.")
        shields = (GameDetailsData().get_armor_data())[cs.shields]
        if shields.search(int(serial_number[6:])):
            self._shield = shields.search(int(serial_number[6:]))
        else:
            raise ValueError("This serial number does not exist.")

    @shield.deleter
    def shield(self):
        raise AttributeError("Character must have a shield, and you are trying to delete it.")

    def attack(self):
        """Here we return the speed and strength of the weapon"""
        return self._weapon.speed(), self._weapon.strength()

    def defend(self):
        """Here we return the speed and strength of the shield"""
        return self._shield.speed(), self._shield.strength()
