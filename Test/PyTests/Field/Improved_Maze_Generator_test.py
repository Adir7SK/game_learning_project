import pytest

from src.Field.Improved_Maze_Generator import Maze


@pytest.mark.parametrize("height, width, expected_dimensions",
                         [(8, 9, (8, 9)),
                          (11, 12, (11, 12)),
                          (100, 150, (100, 150)),
                          ])
def test_dimensions(height, width, expected_dimensions):
    """Dimensions are as specified, and we are able to tune all parameters"""
    temp = Maze(height, width, time_limit=2).generate_maze()
    assert (len(temp), len(temp[0])) == expected_dimensions


@pytest.mark.parametrize("height, width",
                         [(4, -5),
                          (-1, 2),
                          (0, 3500),
                          (14, 0),
                          (4.5, 5),
                          (15, 22.1),
                          ("H", 3500),
                          (14, [20]),
                          ])
def test_illegal_dimensions(height, width):
    """ValueError when dimensions do not make sense.
    Reason for ValueError in each test case.
    Case 1: Negative Width.
    Case 2: Negative Height.
    Case 3: Zero height.
    Case 4: Zero Width.
    Case 5: Not integer Width.
    Case 6: Not integer Height.
    Case 7: String height.
    Case 8: String Width.
    """
    with pytest.raises(AttributeError):
        Maze(height, width)


@pytest.mark.parametrize("height, width",
                         [(8, 9),
                          (11, 12),
                          (100, 150),
                          ])
def test_paths_in_maze(height, width):
    """
    This test validates that the paths in the maze are making sense. There are 4 asserts:
    1. Validates that the length of the winning path from beginning to boss is the right length.
    2. Validates that there is exactly 1 boss.
    3. Validates that there are walls (i.e. that the main character has places it cannot go to).
    4. That the first position is available (because later that's the start point of the main character).
    """
    temp = Maze(height, width, time_limit=2).generate_maze()
    winning_path_len = sum(x.count(1) for x in temp)
    assert winning_path_len == 3 * max(width, height) - 1
    assert sum(x.count(2) for x in temp) == 1
    assert sum(x.count(0) for x in temp) > 0
    assert temp[0][0] == 1
