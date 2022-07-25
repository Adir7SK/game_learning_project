import abc
from abc import ABCMeta, abstractmethod


class Character(metaclass=ABCMeta):
    """
    Here we will define all the characteristics of a character in the game (all types of characters).
    Includes abstract (need to be overwritten in subclass) and concrete methods (which we call with super()).
    It serves as a common API, for when we get an implementation from a third-party (e.g. plugins) or when working
    on a large project (s.a. this one) or a large team, so they all follow the same structure.

    string_when_attack, string_when_defend

    Tests, see if it fails when instantiating it wrong
    see if it succeeds when instantiating right and if we can change the life remaining
    """

    def __init__(self, max_life, life_remain):
        self._max_life = max_life
        self._life_remain = life_remain

    def life_remain(self):
        """Getter method - returns life character currently has left"""
        return self._life_remain

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
