import random
from src.Common_general_functionalities.common_strings import aid_types
from src.Common_general_functionalities.Gaussian_generated_data import scaled_data
import src.Common_general_functionalities.common_strings as cs


class Aid:

    amount_of_possible_magnitudes = cs.amount_of_possible_magnitudes

    def __init__(self, name, aidtype, magnitude):
        """
        Provided aidtype and magnitude, the initializer will immediately create the following:
                    Aid type to specify which kind help the object will provide
                    Magnitude which is calculated (with random factor) relative to the magnitude input
                    Serial number to get the specific aid ID
        """
        if not (aidtype in aid_types or magnitude in range(self.amount_of_possible_magnitudes)):
            raise ValueError("The magnitude must be between 0-{!r} (including), and the aid type must be a known aid.".format(self.amount_of_possible_magnitudes - 1))
        # The following 3 lines takes appropriate block of random numbers from scaled_data corresponding to magnitude
        episode = int(len(scaled_data)/self.amount_of_possible_magnitudes)
        lower = episode*magnitude
        upper = lower + episode
        value = random.choice(scaled_data[lower:upper])
        self._magnitude = round(value * 100, 2)
        self._serial_number = "Aid" + str(int(self._magnitude))
        self._name = name
        self._aid_type = aidtype

    def serial_number(self):
        return self._serial_number

    def name(self):
        return self._name

    @property
    def aid_type(self):
        return self._aid_type

    @aid_type.setter
    def aid_type(self, value):
        raise AttributeError("It is illegal to change the aid to a different type after creation.")

    @property
    def symbol(self):
        return cs.aid

    @symbol.setter
    def symbol(self, val):
        raise AttributeError("Attribute symbol cannot be changed!")

    @symbol.deleter
    def symbol(self):
        raise AttributeError("Attribute symbol cannot be removed from aid.")

    def activate(self):
        a, m = self._aid_type, self._magnitude
        self._aid_type, self._magnitude = None, 0
        return a, m
