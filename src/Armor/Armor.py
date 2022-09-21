from abc import ABCMeta, abstractmethod
from src.Armor.Armor_Details import ArmorDetails


class Armor(ArmorDetails, metaclass=ABCMeta):
    """
    Here we define the characteristics of any armor object in the game (weapon or shield). Typically, they must have:
    name, weight, material, density, shape, efficient, and sound. These are required when initiating an armor. Using
    ArmorDetails class, each initiated armor will also have (automatically calculated) strength, speed, and serial number.

    Here we use abstract (need to be overwritten in subclass) and concrete methods (which we call with super()).
    It serves as a common API, for when we get an implementation from a third-party (e.g. plugins) or when working
    on a large project (s.a. this one) or a large team, so they all follow the same structure.
    """

    def __init__(self, name, weight, material, density, shape, efficient, sound):
        if type(name) != str:
            raise TypeError("Attribute name must be string type")
        if type(sound) != str:
            print(sound)
            raise TypeError("Attribute sound must be string type")

        super().__init__(material, weight, density, shape, efficient)
        self._name = name
        self._sound = sound
        self._armor_efficiency = 1
        self._energy = 100
        self._strength = super().get_strength()
        self._speed = super().get_speed()
        self._serial_number = str(super().get_serial_number())

    @classmethod
    def __subclasshook__(cls, sub):
        """If a class implements the serial_number method, then it is a subclass of Armor"""
        return hasattr(sub, 'serial_number') and callable(sub.serial_number)

    @abstractmethod                     # Annotating that this should be a getter method when implementing a class
    def name(self):
        pass

    @abstractmethod
    def sound(self):
        pass

    @abstractmethod
    def weight(self):
        pass

    @abstractmethod
    def material(self):
        pass

    @abstractmethod
    def density(self):
        pass

    @abstractmethod
    def armor_efficiency(self):
        """Getter method: returns armors current efficiency in fraction (i.e. percentage divided by 100)"""
        pass

    @abstractmethod
    def renew_armor_efficiency(self):
        """Returns the armor's efficiency to full."""
        pass

    @abstractmethod
    def shape(self):
        pass

    @abstractmethod
    def efficient(self):
        pass

    @abstractmethod
    def strength(self):
        pass

    @abstractmethod
    def speed(self):
        pass

    @abstractmethod
    def serial_number(self):
        """This method navigates to which subtree we should go to: weapon/shield and sword/gun or hand/body shield"""
        pass
