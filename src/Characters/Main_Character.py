import operator
from src.Characters.Good_Character import GoodCharacter

"""
Every character should be able to move, there should be a function, before character moves,
which will say whether the move is legal. The move function shall update the position
of the character given the move. There should then also be a function that will return the character's
current position on the board, in the validation step (which determines whether the character can move
in a certain direction) there should add themselves (in the validation function) the move in that direction.
"""


class MainCharacter(GoodCharacter):

    def __init__(self, life, undercover, ns_position, we_position, *items):
        if items == ():
            super().__init__(life, undercover)
        else:
            print("Entered with items")
            # print([i.serial_number() for i in items])
            super().__init__(life, undercover, *items)
            print("Entered with items")
        self._position = (ns_position, we_position)

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, direction):
        if type(direction) != tuple or len(direction) != 2 or not (direction[0] in [-1, 0, 1] and direction[1] in [-1, 0, 1]):
            raise AssertionError("Invalid move.")
        else:
            self._position = tuple(map(operator.add, self._position, direction))

    @position.deleter
    def position(self):
        raise AttributeError("Position attribute cannot be deleted.")


