from src.Armor.Armor import Armor
import src.Common_general_functionalities.common_strings as cs


class Shield(Armor):

    """
    ATTENSION!! THE STRENGTH FROM SHIELD SHOULD CHANGE, SINCE IT IS USED TO PROTECT FROM AN ATTACK
    WE NEED TO THINK OF A FORMULA, WHERE IT WILL ONLY REDUCE THE DAMAGE FROM AN ATTACK!!

    In this class, efficient=True means that the shield is a body-shield, else it is a hand-shield.
    The goal of this class is to:
    Assign that the subclasses here are defence armors/shields.
    Have an indirect getter and setter methods (without using property decorator) to update the armor's efficiency
    Give a cost of energy after each attack.
    """

    def name(self):
        return self._name

    def serial_number(self):
        """This method gives the serial number sequence (with the string 'Weapon' in the beginning)"""
        return cs.shield + str(self._serial_number)

    def serial_number_int(self):
        """Returns only the integer of the serial_number which is then used to assign the weapon in the tree"""
        return int(self._serial_number)

    def sound(self):
        if self._sound:
            return self._sound
        else:
            return ""

    def weight(self):
        return self._weight

    def material(self):
        return self._material

    def density(self):
        return self._density

    def shape(self):
        return self._shape

    def efficient(self):
        return self._efficient

    def strength(self):
        return self._strength

    def speed(self):
        return self._speed

    def armor_efficiency(self):
        """Getter method: returns armors current efficiency in fraction (i.e. percentage divided by 100)"""
        return self._armor_efficiency

    def armor_efficiency_update(self, damage):
        """Setter method - updates armor's efficiency after usage. The greater the damage on the armor, the less
        efficient the armor will be after the attack. The relation is linear."""
        if type(damage) != float:
            raise TypeError("The damage on the armor is from a wrong data type.")
        if not 0 < damage < 1:
            raise ValueError("The damage has a value outside the range.")
        self._armor_efficiency *= (1-damage)

    def renew_armor_efficiency(self):
        """Returns the armor's efficiency to full."""
        self._armor_efficiency = 1
