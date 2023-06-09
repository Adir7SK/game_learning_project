import pytest
import time
import src.Common_general_functionalities.common_strings as cs

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
    example_universe._initialize_field()
    with pytest.raises(AssertionError):
        example_universe.update_field(move)


@pytest.mark.parametrize("position", [(1.5, 0), (0, 1.5), ("0", 1), (1, "0"), (None, 1), (-1, 0), (2, 1), (-1, -5)])
def test_legal_moves_on_initial_position(example_universe, position):
    """
    Verify a that from initial position we cannot move to either illegal position or position that is more than one
    move away.
    """
    example_universe._initialize_field()
    assert position not in example_universe.legal_moves()


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
    example_universe._initialize_field()
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
    example_universe._initialize_field()
    with pytest.raises(AttributeError):
        if delORset:
            example_universe.energy_spent_per_step = energy
        else:
            del example_universe.energy_spent_per_step


@pytest.mark.parametrize("height, width",
                         [(8, 9),
                          (11, 12),
                          (100, 150),
                          ])
def test_paths_in_maze(height, width):
    """
    This test validates that the paths in the field are making sense. There are 4 asserts:
    1. Validates that the length of paths is the right length.
    2. Validates that there is exactly 1 boss.
    3. Validates that there is exactly 1 main character.
    4. Validates that there are walls (i.e. that the main character has places it cannot go to).
    """
    temp = Universe(width, height, "mArS", 5)
    temp._initialize_field()
    winning_path_len = sum(x.count(cs.path) for x in temp.field)
    assert winning_path_len >= 3 * max(width, height) - 12 # winning path length is 3*max(width,height)-1 (then -1 since main character takes space, and -10 since aids and enemies takes 5 each)
    assert sum(x.count(cs.boss) for x in temp.field) == 1
    assert sum(x.count(cs.main_character) for x in temp.field) == 1
    assert sum(x.count(cs.no_path) for x in temp.field) > 0


def test_field_loads_on_the_fly():
    """
    The attribute field is lazy loader which we want to load "on the fly". This means that when first creating the
    object, there's an empty value in field. And only once we need it, then we load it. Once it is loaded, there's no
    need to load it again, because we remember it from the last time. Therefore, the tests are as follows:
    1. Verify that _field is empty after initiation.
    2. Load the field, record the time, and verify that _field is no longer empty.
    3. Record the time of getting field variable again, and compare the time to the previous time we loaded it.
    """
    uni = Universe(10, 10, "mArS", 5)
    assert uni._field == []
    start_time = time.clock()
    uni.field
    first_load = time.clock() - start_time
    assert uni._field != []
    start_time = time.clock()
    uni.field
    second_load = time.clock() - start_time
    assert first_load >= second_load


@pytest.mark.parametrize("case, move, expected",
                         [(1, (1, 0), (1, 0)),
                          (1, (0, 1), (0, 1)),
                          (2, None, 1),
                          (3, None, 1),
                          (3, (-5, 0), 1),
                          (3, (0, 1.1), 1),
                          (3, (1, 3), 1),
                          (3, [1, 1], 1),
                          (3, 1, 1),
                          (3, "Hello", 1),
                          (3, True, 1),
                          ])
def test_legal_and_illegal_moves(example_universe, case, move, expected):
    """
    Testing the different operations with a character's position. A character moves in the right direction given
    the instruction. Illegal move is raising an error. Delete character's position is impossible.
    """
    example_universe.field
    example_universe._field[1][0], example_universe._field[0][1] = cs.path, cs.path # override field (guarantee there's a path in the place we will test)
    if case == 1:
        example_universe.update_field(move)
        assert example_universe.main_character_position == expected
    elif case == 2:
        with pytest.raises(AttributeError):
            del example_universe.main_character_position
    elif case == 3:
        with pytest.raises(AssertionError):
            example_universe.update_field(move)


@pytest.mark.parametrize("case, move, repetitions, expected",
                         [(True, (0, 1), 5, (0, 5)),
                          (True, (1, 0), 8, (7, 0)),
                          (False, (0, 1), 4, (1, 2)),
                          (False, (-1, 0), 8, (0, 1)),
                          ])
def test_repetitive_moves(example_universe, case, move, repetitions, expected):
    """
    Testing that a character can repeat a certain move, and have a combination of moves.
    Validating that in the case of a wrong input data type, an assertion error is raised.
    """
    import random
    example_universe.field
    for i in range(repetitions):
        # override field (guarantee there's a path in the place we will test)
        example_universe._field[(i+1)*move[0]][(i+1)*move[1]] = cs.path
        example_universe.update_field(move)
    if case:
        example_universe._field[example_universe.main_character_position[0]-1][example_universe.main_character_position[1]] = cs.path
        example_universe.update_field((-1, 0))
        assert example_universe.main_character_position == expected
    else:
        illegal_move = random.choice([None, "Hello", (1, 3)])
        with pytest.raises(AssertionError):
            example_universe.update_field(illegal_move)


@pytest.mark.parametrize("move_1, repetitions_1, move_2, repetitions_2, move_3, repetitions_3, expected",
                         [((0, 1), 5, (1, 0), 8, (0, -1), 3, (8, 2)),
                          ((0, 1), 3, (1, 0), 5, (-1, 0), 4, (1, 3)),
                          ])
def test_repetitive_moves_multiple_directions(example_universe, move_1, repetitions_1, move_2, repetitions_2, move_3,
                                              repetitions_3, expected):
    """
    Testing that a character can repeat a certain move, and have a combination of moves.
    Validating that in the case of a wrong input data type, an assertion error is raised.
    """
    example_universe.field
    last_stop = (0, 0)
    for (repetitions, move) in [(repetitions_1, move_1), (repetitions_2, move_2), (repetitions_3, move_3)]:
        for i in range(repetitions):
            # override field (guarantee there's a path in the place we will test)
            example_universe._field[last_stop[0] + (i+1)*move[0]][last_stop[1] + (i+1)*move[1]] = cs.path
            example_universe.update_field(move)
        last_stop = (last_stop[0] + move[0]*repetitions, last_stop[1] + move[1]*repetitions)
    assert example_universe.main_character_position == expected
