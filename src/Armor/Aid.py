import random
from src.Common_general_functionalities.common_strings import aid_types
from src.Common_general_functionalities.Gaussian_generated_data import scaled_data


class Aid:

    amount_of_possible_magnitudes = 5

    def __init__(self, name, aidtype, magnitude):
        if not (aidtype in aid_types or magnitude in range(self.amount_of_possible_magnitudes)):
            raise ValueError("The magnitude must be between 0-{!r} (including), and the aid type must be a known aid.".format(self.amount_of_possible_magnitudes - 1))
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

    def activate(self):
        return self._aid_type, self._magnitude
