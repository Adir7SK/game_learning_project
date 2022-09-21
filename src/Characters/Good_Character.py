from src.Armor.Aid import Aid
from src.Armor.Shield import Shield
from src.Armor.Weapon import Weapon
from src.Characters.Character import Character
from src.Data_Loading.Data_Placement import DataFromLastSave


class GoodCharacter(Character):
    """
    This class defines a good character in the game. This can either be a character that will help the player or 
    the player's character itself.
    
    Upon initialization there is a check of the input data. There's a validation that the character will carry 
    exactly one weapon and one shield, but has no limit in carrying other aiding items.
    
    If there is no weapon or shield at initialization, the character will automatically have his hand as weapon
    and shield. There are getters, setters and (anti) deleter for weapon, shield and undercover.

    There are methods to get a list of all the items the character has, and methods to get full information
    about the character's weapon and shield.

    For the practical implementation, there is a method that should return the symbol of the current character on
    the map. There is also a method for attack and defend. Both return the speed and strength of the weapon the
    character possesses. These will later determine how much damage they cause to the opponent and how much they
    reduce an attack from the opponent.

    Note!! Weapon class has also energy attribute that hasn't been used anywere (except for in the testing the class).
    This is good to have for the characters, so each movement/attack/defend will reduce the energy. Please look at the
    implementation in Weapon class.

    The items (which you can add as many as you want when initiating a character class) are a collection of
    Weapon, Shield, and Aids. Each such item will consist of a list with 2 elements: serial code and object
    """
    def __init__(self, life, undercover,  *items):
        if type(undercover) != bool:
            raise TypeError("Character's undercover value must be a boolean value.")
        self._weapon, self._shield, self.aids = None, None, []
        for item in items:
            if not isinstance(item, (Aid, Shield, Weapon)):
                raise AttributeError("Attributes after undercover must be either Aid, Weapon, or Shield type.")
            serial_number = item.serial_number()
            if serial_number[:6] not in ["Weapon", "Shield"] and serial_number[:3] != "Aid":
                raise AttributeError("The items a character can carry are either a Weapon, Shield, or an Aid.")
            if serial_number[:6] == "Weapon":
                if self._weapon:
                    raise AttributeError("Character must have one weapon at most.")
                else:
                    self._weapon = item
            elif serial_number[:6] == "Shield":
                if self._shield:
                    raise AttributeError("Character must have one shield at most.")
                else:
                    self._shield = item
            else:
                self.aids.append(item)

        if not self._weapon:
            weapons = (DataFromLastSave().get_armor_data())["Weapons"]
            i = 1
            while not weapons.search(i):
                i += 1
            self._weapon = weapons.search(i)
        if not self._shield:
            shields = (DataFromLastSave().get_armor_data())["Shields"]
            i = 1
            while not shields.search(i):
                i += 1
            self._shield = shields.search(i)

        super().__init__(life)
        self._undercover = undercover
        self._energy = 100

    def items(self):                  # This kind of character must have a weapon, shield, and potentially more items.
        """List of items that character carries"""
        available_items = [(self._weapon.name(), self._weapon.serial_number()), (self._shield.name(), self._shield.serial_number())]
        for item in self.aids:
            available_items.append((item.name(), item.serial_number()))
        return available_items

    @property
    def symbol(self):
        """The symbol on the printed maze that identifies the character"""
        raise NotImplementedError
    
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
        if serial_number[:6] != "Weapon":
            raise ValueError("Invalid weapon serial number. Valid example: Weapon460.")
        weapons = (DataFromLastSave().get_armor_data())["Weapons"]
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
        if serial_number[:6] != "Shield":
            raise ValueError("Invalid shield serial number. Valid example: Shield460.")
        shields = (DataFromLastSave().get_armor_data())["Shields"]
        if shields.search(int(serial_number[6:])):
            self._shield = shields.search(int(serial_number[6:]))
        else:
            raise ValueError("This serial number does not exist.")

    @shield.deleter
    def shield(self):
        raise AttributeError("Character must have a shield, and you are trying to delete it.")

    @property
    def energy(self):
        """Using armor costs some energy. This method returns the remaining energy."""
        return self._energy

    @energy.setter
    def energy(self, value):
        """
        The amount of energy being subtracted for each attack or step.
        Here we consider the possibility that the character might just take a step in the current planet,
        which leads to energy reduction of gravity divided by 5. In this case, the input should be True and
        the gravity of the planet (positive float value). The other possibility is an attack/defence. If so,
        the reduction will be the weight of the corresponding armor. If it is an attack, the input will be
        [False, 1], if it is defence, the input will be [False, 0].
        """
        if len(value) != 2:
            raise AttributeError("There must be a list with two inputs.")
        if type(value[0]) != bool:
            raise TypeError("The first input must be a boolean: True for step and False for attack/defence.")
        if not isinstance(value[1], (float, int)):
            raise TypeError("The second input must be a number (int/float).")
        if value[0]:
            self._energy = max(self._energy - (value[1]/5), 0)
        elif value[1] == 1:
            self._energy = max(self._energy - self._weapon.weight(), 0)
        else:
            self._energy = max(self._energy - self._shield.weight(), 0)

    @energy.deleter
    def energy(self):
        raise AttributeError("You are not allowed to delete the energy attribute.")

    def renew_energy(self):
        """Returns the armor's energy to full."""
        self._energy = 100

    def attack(self):
        """Here we return the speed and strength of the weapon"""
        return self._weapon.speed(), self._weapon.strength()

    def defend(self):
        """Here we return the speed and strength of the shield"""
        return self._shield.speed(), self._shield.strength()

    def weapon_info(self):
        """This should return relevant information about the weapon."""
        print("Your weapon has the following details:")
        print("Name:           ", self._weapon.name())
        print("Serial Number:  ", self._weapon.serial_number())
        print("Speed:          ", self._weapon.speed())
        print("Strength:       ", self._weapon.strength())
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

    def aids_info(self):
        """This should return relevant information about all the aids this character has."""
        raise NotImplementedError

