from src.Common_general_functionalities.common_strings import possible_materials, possible_shapes
from src.Common_general_functionalities.Gaussian_generated_data import scaled_data
from src.Common_general_functionalities import Flexible_Attributes as fa


class ArmorDetails:
    """
    This class generates strength, speed and serial_number based on armor's Shape, Material, Density, and
    type (gun/sword or body/hand shield).
    With the slots method and the use of super and setattr, we are making this class to an immutable class
    """
    def __init__(self, *args):
        if len(args) != 5:
            raise TypeError("Missing data at initiation of this armor.")
        if args[0] not in possible_materials:
            raise ValueError("The material does not exist.")
        if (not isinstance(args[1], (float, int))) or args[1] <= 0 or type(args[1]) == bool:
            raise ValueError("The weight must be a positive float.")
        if (not isinstance(args[2], (float, int))) or type(args[2]) == bool or not 0 < args[2] < 100:
            raise ValueError("The density must be a positive number smaller than 100.")
        if type(args[3]) != str or len(args[3].split(" ")) != 2:
            raise ValueError("The shape must consist of a two words string.")
        detail1, detail2 = args[3].split(" ")
        if detail1 == detail2 or detail1 not in possible_shapes.keys() or detail2 not in possible_shapes.keys():
            raise ValueError("The shape's details do not exist")
        if type(args[4]) != bool:
            raise TypeError("When determining the details of an armor, efficiency tells whether it is an efficient "
                            "armor or not. Hence must be True/False..")

        attributes_names = ["material", "weight", "density", "shape", "efficient"]
        private_coords = {'_' + attributes_names[i]: args[i] for i in range(len(attributes_names))}
        self.__dict__.update(private_coords)

    def __getattr__(self, name):
        private_name = '_' + name  # With this we don't need to add underscore when we are looking for the attribute
        try:
            return self.__dict__[private_name]
        except KeyError:
            raise AttributeError('{!r} object has no attribute {!r}'.format(self.__class__, name))
        #return getattr(self, private_name)

    def __setattr__(self, key, value):
        if key in self.__dict__ and key not in fa.flexible_in_armor:
            raise AttributeError(f"Cannot change this attribute.")
        else:
            self.__dict__.update({key: value})

    def __delattr__(self, name):  # The method added
        raise AttributeError(
            "Can't delete attribute {!r}".format(name))  # Error message when trying to delete attribute

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__, ', '.join(
            "{k}={v}".format(k=k[1:], v=self.__dict__[k]) for k in sorted(self.__dict__.keys())))

    def get_strength(self):
        """
        This method returns the strength of an armor based on its material, weight, shape, density, and efficiency.
        The above are mapped to values (we do not use traditional encodings for string values, but rather
        manually assigning a value for each string).
        The mapping is as follows:
        Material: String -> int between 1 and 13
        Weight: float -> float manipulation (further away from 2 gets higher value) with range between 0.01 and 2
        Shape: String -> int between 2 and 6
        Density: float -> float

        Then we get the first score:  material*weight*shape*density  and add 15600 points if it is an efficient armor.
        Uniformly rescale to be number between 0 and 1.

        Taking the rescaled value, and find the corresponding bucket from the normal distribution (i.e. scaled_data
        contains sorted numbers between 0 and 1 where there are more numbers around 0.5 and fewer numbers around the
        edges), which has a number. The final result is that buckets value * 50.

        Output: values below 25 are inefficient armor (e.g. sword or hand shield) while values above 25 are the
        efficient armor (e.g. gun or body shield). From there, the lower the value is, the worse armor it is (made
        of cheap wood with bad shape and terrible weight) and the higher the value is, the better the armor is.
        """
        material_score = 1 + possible_materials.index(self._material)
        weight_score = max(abs(2 - self._weight), 0.01)
        if self._weight > 2:
            weight_score = max(weight_score/5, 0.01)
        detail1, detail2 = self._shape.split(" ")
        shape_score = possible_shapes[detail1] + possible_shapes[detail2]
        score = material_score * weight_score * shape_score * self._density
        if self._efficient:
            score += 15600
        scaled_score = score / 31200
        for s in scaled_data:
            if scaled_score <= s:
                return s*50
        return 50

    def get_speed(self):
        """
        This method returns the speed of an armor based on its weight, shape, and efficiency.
        The above are mapped to values (we do not use traditional encodings for string values, but rather
        manually assigning a value for each string).
        The mapping is as follows:
        Weight: float -> number manipulation to another float (further away from the value 2 gets higher value)
        Shape: String -> int between 2 and 6

        Then we get the first score:  weight*shape      and add 100 points if it is an efficient armor.
        Uniformly rescale to be number between 0 and 1.

        Taking the rescaled value, and find the corresponding bucket from the normal distribution (i.e. scaled_data
        contains sorted numbers between 0 and 1 where there are more numbers around 0.5 and fewer numbers around the
        edges), which has a number. The final result is that buckets value * 10.

        Output: values below 5 are inefficient armor (e.g. sword or hand shield) while values above 5 are the
        efficient armor (e.g. gun or body shield). From there, the lower the value is, the worse armor it is (made
        of cheap wood with bad shape and terrible weight) and the higher the value is, the better the armor is.
        """
        weight_score = max(abs(2 - self._weight), 0.01)
        if self._weight > 2:
            weight_score = max(weight_score / 5, 0.01)
        detail1, detail2 = self._shape.split(" ")
        shape_score = possible_shapes[detail1] + possible_shapes[detail2]
        score = weight_score * shape_score
        if self._efficient:
            score += 20
        scaled_score = score / 32
        for s in scaled_data:
            if scaled_score <= s:
                return s*10
        return 10

    def get_serial_number(self):
        """
        Here we get a serial number based on the strength and the speed of the armor.
        """
        strength = self.get_strength()
        speed = self.get_speed()
        return int(strength * speed * 10)

