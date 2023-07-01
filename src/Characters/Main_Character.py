from src.Characters.Good_Character import GoodCharacter
import src.Common_general_functionalities.common_strings as cs
from src.Armor.Aid import Aid
from src.Armor.Shield import Shield
from src.Armor.Weapon import Weapon


class MainCharacter(GoodCharacter):
    """
    This is the only character the player can directly control.

    Its inputs are:

    Life = The initial amount of life and maximum life the character has (int/float).
    undercover = Whether the character is undercover (boolean).
    items = List of all the items the character can carry - character can carry up to one weapon and one shield,
                but unlimited aid items (Aid, Weapon, or Shield class)


    The methods it has are:
    life - Getter, setter, and deleter to amount of remaining life the character currently has (float/integer >=0).
    alive - Whether the character is alive or dead. There's also possibility to resurrect/immediate kill (boolean).
    items - List of tuples with all the items the character has. Each tuple has item's name and item's serial number.
    symbol - Character's symbol on the map (String).
    undercover - Whether the character is undercover or not - this is still subject for change, since this character
                 will never be undercover (boolean) - perhaps in the future an element of invisible to the enemies will
                 come to play.
    weapon - Getter, setter, and deleter to return/change the weapon the character is using (Weapon Object)
    shield - Getter, setter, and deleter to return/change the shield the character is using (Shield Object)
    energy - Getter, setter, and deleter to return/change the character's energy (float/int between 0-100).
    renew_energy - recharging the energy to full (float/int).
    attack - returning the weapon's strength, speed, and efficiency (3 floats).
    defend - returning the shield's strength, speed, and efficiency (3 floats).

    Unique to this character:
    recharge_life - Increasing the character's current amount of life, considering upper limit of full_life (float/int).
    full_life - Getter, setter, and deleter for the maximum life a character can have (float/int).
    position - Getter, setter, and deleter for the position of the character (tuple of 2 integer).
    weapon_info - Directly prints all the information about the character's weapon.
    shield_info - Directly prints all the information about the character's shield.
    character_info - Directly prints all the information about the character.
    """
    def __init__(self, life, *items):
        if items == ():
            super().__init__(life, False)
        else:
            super().__init__(life, False, *items)
        self._strength = 5
        self._speed = 5

    def recharge_life(self, recharge_pack):
        """This method gives the option to recharge a character's life, with the upper bound of maximum life."""
        if not type(recharge_pack) in [float, int]:
            raise TypeError("The recharge amount must be float or int.")
        elif self._alive:
            self._life = min(self._full_life, self._life + recharge_pack)

    def add_item(self, item):
        """This gives the possibility for a character to have more items in their bag."""
        if not (isinstance(item, Aid) or isinstance(item, Weapon) or isinstance(item, Shield)):
            raise TypeError("You can only add Aid type items.")
        if item.serial_number() in self.aids.keys():
            print("You cannot have twice an item with the same serial number.")
        else:
            self.aids[item.serial_number()] = item

    def _remove_item(self, item_id):
        """This is a method to remove item from the bag collection. Input is item's serial number."""
        del self.aids[item_id]

    @property
    def full_life(self):
        """Getter method - returns the maximum life this character can have."""
        return self._full_life

    @full_life.setter
    def full_life(self, max_life):
        """Setter method to updates maximum life this character can have."""
        if (not type(max_life) in [float, int]) or max_life <= 0:
            raise TypeError("Character's life must be a positive number: {!r}, {!r}".format(max_life, type(max_life)))
        self._full_life = max_life

    @full_life.deleter
    def full_life(self):
        raise AttributeError("Maximum life is an attribute that cannot be deleted.")

    @property
    def symbol(self):
        """The symbol on the printed maze that identifies the character"""
        return cs.main_character

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, improvement):
        if type(improvement) not in [int, float]:
            raise TypeError("Strength must be integer or float.")
        if self._speed + improvement < 0:
            self._speed = 0
        else:
            self._speed += improvement

    @speed.deleter
    def speed(self):
        raise AttributeError("Speed attribute cannot be deleted.")

    @property
    def strength(self):
        return self._strength

    @strength.setter
    def strength(self, improvement):
        if type(improvement) not in [int, float]:
            raise TypeError("Strength must be integer or float.")
        if self._strength + improvement < 0:
            self._strength = 0
        else:
            self._strength += improvement

    @strength.deleter
    def strength(self):
        raise AttributeError("Strength attribute cannot be deleted.")

    def attack(self):
        w_speed, w_strength, w_efficiency = super().attack()
        return w_speed+self.speed, w_strength+self.strength, w_efficiency

    def defend(self):
        s_speed, s_strength, s_efficiency = super().defend()
        return s_speed+self.speed, s_strength+self.strength, s_efficiency

    def use_aid(self, aid_serial):
        """
        aid is a tuple of 2 elements, name and serial number.
        This method activates the aid for the benefit of the player.
        """
        if aid_serial not in self.aids.keys():
            return
        aid = self.aids[aid_serial]
        if aid_serial.startswith('Aid'):
            aid_type, magnitude = aid.activate()
            if aid_type == cs.health:
                self.recharge_life(magnitude)
            elif aid_type == cs.energy:
                self.renew_energy()
            elif aid_type == cs.strength:
                self.strength += magnitude
            elif aid_type == cs.speed:
                self.speed += magnitude
            elif aid_type == cs.full_life:
                self.full_life += magnitude
        elif aid_serial.startswith(cs.weapon):
            self.weapon = aid_serial
        elif aid_serial.startswith(cs.shield):
            self.shield = aid_serial
        self._remove_item(aid_serial)

    def weapon_info(self):
        """This should return relevant information about the weapon."""
        print("Your weapon has the following details:")
        print("Name:           ", self._weapon.name())
        print("Serial Number:  ", self._weapon.serial_number())
        print("Speed:          ", self._weapon.speed() + self._speed)
        print("Strength:       ", self._weapon.strength() + self._strength)
        print("Weapon's state: ", self._weapon.armor_efficiency()*100)
        print("Weight:         ", self._weapon.weight())
        print("Shape:          ", self._weapon.shape())
        print("Material:       ", self._weapon.material())
        print("Density:        ", self._weapon.density())

    def shield_info(self):
        """This should return relevant information about the shield."""
        print("Your shield has the following details:")
        print("Name:           ", self._shield.name())
        print("Serial Number:  ", self._shield.serial_number())
        print("Speed:          ", self._shield.speed())
        print("Strength:       ", self._shield.strength())
        print("Shield's state: ", self._shield.armor_efficiency() * 100)
        print("Weight:         ", self._shield.weight())
        print("Shape:          ", self._shield.shape())
        print("Material:       ", self._shield.material())
        print("Density:        ", self._shield.density())

    def short_armor_info(self):
        print("Shield Info:")
        print("Name:           ", self._shield.name())
        print("Speed:          ", self._shield.speed())
        print("Strength:       ", self._shield.strength())
        print("Shield's state: ", self._shield.armor_efficiency() * 100)
        print("Weapon Info:")
        print("Name:           ", self._weapon.name())
        print("Speed:          ", self._weapon.speed())
        print("Strength:       ", self._weapon.strength())
        print("Weapon's state: ", self._weapon.armor_efficiency() * 100)

    def character_info(self):
        """This should return relevant information about the shield."""
        print("Thies character's details are:")
        print("Life remaining:    ", self._life)
        print("Max possible Life: ", self._full_life)
        print("Strength:          ", self._strength)
        print("Speed:             ", self._speed)
        print("Energy left:       ", self._energy)
        print("Items:             ", self.items())
        print("Shield name: {0}. It's Serial Number: {1}".format(self._shield.name(), self._shield.serial_number()))
        print("Weapon name: {0}. It's Serial Number: {1}".format(self._weapon.name(), self._weapon.serial_number()))
