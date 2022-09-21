import abc
from abc import ABCMeta, abstractmethod


class Character(metaclass=ABCMeta):
    """
    Here we will define all the characteristics of a character in the game (all types of characters).
    """

    def __init__(self, life):
        if life <= 0 or not type(life) in [float, int]:
            raise TypeError("Character's life must be a positive number: {!r}, {!r}".format(life, type(life)))
        self._life = life

    @property
    def life_remain(self):
        """Getter method - returns life character currently has left"""
        return self._life

    @life_remain.setter
    def life_remain(self, damage):
        """Setter method to updates life after attack"""
        if type(damage) != int and type(damage) != float:
            raise TypeError("The attack is from a wrong data type.")
        self._life -= damage

    @life_remain.deleter
    def life_remain(self):
        raise AttributeError("Life remaining is an attribute that cannot be deleted.")

    @abc.abstractmethod
    def items(self):
        """List of items that character carries"""
        pass

    @abstractmethod
    def symbol(self):
        """The symbol on the printed maze that identifies the character"""
        pass
