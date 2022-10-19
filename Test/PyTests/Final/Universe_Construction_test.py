import pytest

from src.Final.Universe_Construction import Universe

"""
test illegal input types (for init and all the other methods)       V
test illegal moves                                                  V
test field property                                                 V
test energy_spent_per_step                                          V
test legal_to_move                                                  V
test update_field                                                   V
test whether all the functions work when they should
"""


@pytest.fixture
def example_universe():
    """This function gives a universe data fixture."""
    return Universe(10, 10, "mArS", 5)


@pytest.mark.parametrize("dim_y, dim_x, planet, level",
                         [(-1, 10, "Pluto", 2),
                          (10.5, 10, "Pluto", 2),
                          ("10", 10, "Pluto", 2),
                          ([10], 10, "Pluto", 2),
                          (None, 10, "Pluto", 2),
                          (10, -10, "Pluto", 2),
                          (10, 10.2, "Pluto", 2),
                          (10, "10", "Pluto", 2),
                          (10, [10], "Pluto", 2),
                          (10, None, "Pluto", 2),
                          (10, 10, "Pluti", 2),
                          (10, 10, ["Pluto"], 2),
                          (10, 10, None, 2),
                          (10, 10, "Pluto", -2),
                          (10, 10, "Pluto", 2.2),
                          (10, 10, "Pluto", "2"),
                          (10, 10, "Pluto", None),
                          ])
def test_init_illegal_input_attribute(dim_y, dim_x, planet, level):
    """Initializing with wrong data type leads to an Attribute Error."""
    with pytest.raises(AttributeError):
        Universe(dim_y, dim_x, planet, level)


@pytest.mark.parametrize("dim_y, dim_x, planet, level",
                         [(5, 10, "Pluto", 2),
                          (10, 5, "Pluto", 2),
                          ])
def test_init_illegal_input_value(dim_y, dim_x, planet, level):
    """Initializing with wrong data type leads to an Attribute Error."""
    with pytest.raises(ValueError):
        Universe(dim_y, dim_x, planet, level)


@pytest.mark.parametrize("move", [(1.5, 0), (0, 1.5), ("0", 1), (1, "0"), (None, 1), (1, None), (2, 1), (-1, -5)])
def test_update_field_illegal_move(example_universe, move):
    """Trying to move with illegal input."""
    example_universe.initialize_field()
    with pytest.raises(AttributeError):
        example_universe.update_field(move)


@pytest.mark.parametrize("move", [(1.5, 0), (0, 1.5), ("0", 1), (1, "0"), (None, 1), (1, None), (2, 1), (-1, -5), (1, 0)])
def test_legal_to_move_illegal_move(example_universe, move):
    """Trying to verify a move from a certain position that do not match the player's current position."""
    example_universe.initialize_field()
    with pytest.raises(AttributeError):
        example_universe.legal_to_move(move)


@pytest.mark.parametrize("delORset, field",
                         [(0, 0),
                          (1, 1.5),
                          (1, 1),
                          (1, "0"),
                          (1, [0]),
                          (1, None),
                          (1, 2),
                          ])
def test_field_properties(example_universe, delORset, field):
    """Trying to verify a move from a certain position that do not match the player's current position."""
    example_universe.initialize_field()
    if not delORset:
        with pytest.raises(AttributeError):
            del example_universe.field
    else:
        with pytest.raises(AttributeError):
            if field != 2:
                example_universe.field = field
            else:
                example_universe.field = [[0 for _ in range(10)] for _ in range(10)]


@pytest.mark.parametrize("delORset, energy",
                         [(0, 0),
                          (1, 1.5),
                          (1, 1),
                          (1, "0"),
                          (1, [0]),
                          (1, None),
                          ])
def test_field_properties(example_universe, delORset, energy):
    """Trying to verify a move from a certain position that do not match the player's current position."""
    example_universe.initialize_field()
    with pytest.raises(AttributeError):
        if delORset:
            example_universe.energy_spent_per_step = energy
        else:
            del example_universe.energy_spent_per_step
