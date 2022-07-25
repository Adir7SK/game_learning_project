import abc
from abc import ABCMeta, abstractmethod


class Character(metaclass=ABCMeta):
    """
    Here we will define all the characteristics of a character in the game (all types of characters).
    """

    def __init__(self, max_life, life_remain):
        self._max_life = max_life
        self._life_remain = life_remain

    @property
    def life_remain(self):
        """Getter method - returns life character currently has left"""
        return self._life_remain

    @life_remain.setter
    def life_remain(self, damage):
        """Setter method to updates life after attack"""
        if type(damage) != int and type(damage) != float:
            raise TypeError("The attack is from a wrong data type.")
        self._life_remain -= damage

    @abc.abstractmethod
    def items(self):
        """List of items that character carries"""
        pass

    @abstractmethod
    def symbol(self):
        """The symbol on the printed maze that identifies the character"""
        pass
