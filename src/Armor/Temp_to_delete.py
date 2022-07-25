__slots__ = "_material", "_weight", "_density", "_shape", "_efficient"


def __init__(self, material, weight, density, shape, efficient):
    if material not in possible_materials:
        raise ValueError("The material does not exist.")
    if (not isinstance(weight, (float, int))) or weight <= 0:
        raise ValueError("The weight must be a positive float.")
    if (not isinstance(density, (float, int))) or density <= 0 or density > 100:
        raise ValueError("The density must be a positive float.")
    if type(shape) != str or len(shape.split(" ")) != 2:
        raise ValueError("The shape must consist of a two words string.")
    detail1, detail2 = shape.split(" ")
    if detail1 == detail2 or detail1 not in possible_shapes.keys() or detail2 not in possible_shapes.keys():
        raise ValueError("The shape's details do not exist")
    if type(efficient) != bool:
        raise TypeError("When determining the details of an armor, efficiency tells whether it is an efficient "
                        "armor or not. Hence must be True/False..")

    super(ArmorDetails, self).__setattr__("_material", material)
    super(ArmorDetails, self).__setattr__("_weight", weight)
    super(ArmorDetails, self).__setattr__("_density", density)
    super(ArmorDetails, self).__setattr__("_shape", shape)
    super(ArmorDetails, self).__setattr__("_efficient", efficient)


def __setattr__(self, key, value):
    """"""
    if key in ["material", "weight", "density", "shape", "efficient"]:
        msg = "'%s' cannot change attribute '%s' after initiation." % (self.__class__, key)
        raise AttributeError(msg)

    ###########################################################
    ######### This is the original setattr ####################
    ###########################################################
    def __setattr__(self, name, value):
        raise AttributeError("Can't set attribute {!r}".format(
            name))  # Now it is impossible to change a value of an attribute (or add an attribute)

# NOTE: try to use @abs.abstract method in order to specify that you'll have a decorator in the inherited/child class
