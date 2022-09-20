from Character import Character
from src.Final.Data_Placement import DataFromLastSave


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
        self._weapon_serial, self._shield_serial, self.aids_serial = None, None, []
        self._weapon, self._shield, self.aids = None, None, []
        for code_and_object in items:
            if len(code_and_object) != 2:
                raise AttributeError("All inputs after undercover attribute must be a list of 2 items.")
            serial_number = code_and_object[0]
            if serial_number[:6] not in ["Weapon", "Shield"] and serial_number[:3] != "Aid":
                raise ValueError("The items a character can carry are either a Weapon, Shield, or an Aid.")
            if serial_number[:6] == "Weapon":
                if self._weapon_serial:
                    raise AttributeError("Character must have one weapon at most.")
                else:
                    self._weapon_serial = serial_number
                    self._weapon = code_and_object[1]
            elif serial_number[:6] == "Shield":
                if self._shield_serial:
                    raise AttributeError("Character must have one shield at most.")
                else:
                    self._shield_serial = serial_number
                    self._shield = code_and_object[1]
            else:
                self.aids_serial.append(serial_number)
                self.aids.append(code_and_object[1])

        if not self._weapon_serial:
            weapons = (DataFromLastSave().get_armor_data())["Weapons"]
            i = 1
            while not weapons.search(i):
                i += 1
            self._weapon = weapons.search(i)
            self._weapon_serial = self._weapon.serial_number()
        if not self._shield_serial:
            shields = (DataFromLastSave().get_armor_data())["Shields"]
            i = 1
            while not shields.search(i):
                i += 1
            self._shield = shields.search(i)
            self._shield_serial = self._shield.serial_number()

        super().__init__(life)
        self._undercover = undercover

    def items(self):                  # This kind of character must have a weapon, shield, and potentially more items.
        """List of items that character carries"""
        available_items = [self._weapon.name(), self._shield.name()]
        for item in self.aids:
            available_items.append(item.name())
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
            raise ValueError("The undercover value must be boolean.")

    @property
    def weapon(self):
        return self._weapon

    @weapon.setter
    def weapon(self, serial_number):
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
        shields = (DataFromLastSave().get_armor_data())["Shields"]
        if shields.search(int(serial_number[6:])):
            self._shield = shields.search(int(serial_number[6:]))
        else:
            raise ValueError("This serial number does not exist.")

    @shield.deleter
    def shield(self):
        raise AttributeError("Character must have a shield, and you are trying to delete it.")

    @property
    def attack(self):
        """Here we return the speed and strength of the weapon"""
        return self._weapon.speed(), self._weapon.strength()

    @property
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


if __name__ == '__main__':
    character = GoodCharacter(1200, True)
    character.life_remain = 12
    print(character.life_remain)
    print(character.attack)
    character.weapon_info()
    # del character.life_remain

