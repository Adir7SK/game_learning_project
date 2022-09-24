import abc
from abc import ABCMeta, abstractmethod


class Character(metaclass=ABCMeta):
    """
    Here we will define all the characteristics of a character in the game (all types of characters).
    """

    def __init__(self, life):
        if (not type(life) in [float, int]) or life <= 0:
            raise TypeError("Character's life must be a positive number: {!r}, {!r}".format(life, type(life)))
        self._life = life
        self._full_life = life
        self._alive = True

    @property
    def life(self):
        """Getter method - returns life character currently has left"""
        return self._life

    @life.setter
    def life(self, damage):
        """Setter method to updates life after attack"""
        if not type(damage) in [int, float]:
            raise TypeError("The attack is from a wrong data type.")
        self._life = max(0, self._life - damage)
        if self._life == 0:
            self._alive = False

    @life.deleter
    def life(self):
        raise AttributeError("Life remaining is an attribute that cannot be deleted.")

    @property
    def alive(self):
        """Getter method - returns whether a character is alive or not."""
        return self._alive

    @alive.setter
    def alive(self, resurrect):
        """Setter method to updates maximum life this character can have."""
        if type(resurrect) == bool:
            self._alive = resurrect
            if resurrect:
                self._life = self._full_life
            else:
                self._life = 0
        else:
            raise TypeError("Input for character alive or dead can only be True or False")

    @alive.deleter
    def alive(self):
        raise AttributeError("Maximum life is an attribute that cannot be deleted.")

    @abc.abstractmethod
    def items(self):
        """List of items that character carries"""
        pass

    @abstractmethod
    def symbol(self):
        """The symbol on the printed maze that identifies the character"""
        pass
