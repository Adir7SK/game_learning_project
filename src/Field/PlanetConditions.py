from weakref import WeakKeyDictionary


class Named:

    def __init__(self, name=None) -> None:
        self.name = name


class Positive(Named):
    """
    This will serve as a descriptor.
    It covers get, set, and delete functionalities for planets + vlidate the values

    Values will be associated with the Planet class and not the instances (e.g. Pluto), therefore we need a weak
    reference, otherwise, when changing the value, all instances will also chang (e.g. if changing Pluto's mass it'll
    also change the mass of Mars, Jupyter...)
    """
    def __init__(self, name=None):
        super().__init__(name)               # We take the init (constructor) function from the previous (Named) class.
        self._instance_data = WeakKeyDictionary()

    def __get__(self, instance, owner):
        # If no instance is specified when getting info (e.g. instead of pluto.mass the user types Planet.mass),
        # return descriptor. To get the class holding the descriptor, we would use self.owner
        if instance == None:
            return self
        return self._instance_data[instance]

    def __set__(self, instance, value):
        if value <= 0:
            raise ValueError("Attribute value {} {} is not positive".format(self.name, value))
        self._instance_data[instance] = value

    def __delete__(self, instance):
        raise AttributeError("Cannot delete attribute {}".format(self.name))


# Metaclass to detect the presence of named descriptors, and assign class attribute names to them
class DescriptorNamingMeta(type):
    """
    The metaclass detects the presence of named descriptors, and assign class attribute names to them.
    It will be used to identify which attribute got an invalid value.
    E.g. without it, if radius gets invalid value, we'll get an error, but in the error
    we won't know that it was radius that had the invalid value.
    """
    # Method invoked before __init__ to create the class (mcs is the key word for metaclass - like cls for class)
    def __new__(mcs, name, bases, namespace):
        for name, attr in namespace.items():
            if isinstance(attr, Named):
                attr.name = name        # if the attribute from the namespace dictionary is instance of named we assign the name of the current item to its public name attribute
            return super().__new__(mcs, name, bases, namespace)     # This is to allocate the class object


class Planet(metaclass=DescriptorNamingMeta):
    """
    In this class we define planets
    """
    def __init__(self, name, mass, radius, temperature_kelvin) -> None:
        self.name = name
        self.mass = mass
        self.radius = radius
        self.temperature_kelvin = temperature_kelvin
        self.gravitational_force = self.gravity()

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not value:
            raise ValueError("Invalid name value")
        self._name = value

    def gravity(self):
        g = 6.67e-11                        # Gravitational constant
        return round((g * self.mass) / (self.radius**2), 2)

    mass = Positive()
    radius = Positive()
    temprature_kelvin = Positive()


# Here we create the planets we will need - in order from easiest planet to hardest
planets = {
    "pluto": Planet(name='Pluto', radius=1184e3, mass=1.309e22, temperature_kelvin=50),
    "mars": Planet(name='Mars', radius=3389.5e3, mass=6.39e23, temperature_kelvin=210),
    "mercury": Planet(name='Mercury', radius=2439.7e3, mass=3.285e23, temperature_kelvin=440),
    "venus": Planet(name='Venus', radius=6052e3, mass=4.867e24, temperature_kelvin=737),
    "earth": Planet(name='Earth', radius=6371e3, mass=5.972e24, temperature_kelvin=288),
    "uranus": Planet(name='Uranus', radius=25362e3, mass=8.681e25, temperature_kelvin=76),
    "saturn": Planet(name='Saturn', radius=58232e3, mass=5.683e26, temperature_kelvin=134),
    "neptune": Planet(name='Neptune', radius=24622e3, mass=1.024e26, temperature_kelvin=72),
    "jupiter": Planet(name='Jupiter', radius=69911e3, mass=1.898e27, temperature_kelvin=165),
}
