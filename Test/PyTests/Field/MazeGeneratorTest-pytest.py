import pytest
import numpy.testing as npt
from src.Field.MazeGenerator import dim, create_maze


@pytest.mark.parametrize("height, width, p, expected_dimensions",
                         [(4, 5, 0.2, (12, 15)),
                          (1, 2, 0.5, (3, 6)),
                          (200, 350, 0.8, (600, 1050)),
                          ])
def test_dimensions(height, width, p, expected_dimensions):
    """Dimensions are as specified, and we are able to tune all parameters"""
    assert dim(create_maze(height, width, p)) == expected_dimensions


@pytest.mark.parametrize("height, width, edge",
                         [(4, 5, "R"),
                          (4, 5, "B"),
                          (4, 5, "U"),
                          (4, 5, "L"),
                          (11, 7, "L"),
                          (11, 7, "U"),
                          (11, 7, "B"),
                          (11, 7, "R"),
                          ])
def test_edges(height, width, edge):
    """Testing that all the edges of a maze are always walls (represented by #)
    First 4 tests are for a 4 X 5 size maze and the last 4 tests are for 11 X 7 size maze:
    Case 1: Testing whether the most right edge of the maze is solely a wall.
    Case 2: Testing whether the lowest edge of the maze is solely a wall.
    Case 3: Testing whether the upper edge of the maze is solely a wall.
    Case 4: Testing whether the most left edge of the maze is solely a wall.
    Case 5: Testing whether the most left edge of the maze is solely a wall.
    Case 6: Testing whether the upper edge of the maze is solely a wall.
    Case 7: Testing whether the lower edge of the maze is solely a wall.
    Case 8: Testing whether the most right edge of the maze is solely a wall.
    """
    maze = create_maze(height, width)
    if edge == "U": correct_edge, maze_part = ['#'] * len(maze[0]), maze[0]
    elif edge == "B": correct_edge, maze_part = ['#'] * len(maze[0]), maze[len(maze)-1]
    elif edge == "R": correct_edge, maze_part = ['#'] * len(maze), maze[:, len(maze[0]) - 1]
    elif edge == "L": correct_edge, maze_part = ['#'] * len(maze), maze[:, 0]
    npt.assert_array_equal(maze_part, correct_edge)


@pytest.mark.parametrize("height, width, p",
                         [(4, -5, 0.5),
                          (-1, 2, 0.2),
                          (0, 3500, 0.4),
                          (14, 0, 0.8),
                          (14, 10, -0.8),
                          (14, 10, 8),
                          ])
def test_illegal_dimensions(height, width, p):
    """ValueError when dimensions do not make sense.
    Reason for ValueError in each test case.
    Case 1: Negative Width.
    Case 2: Negative Height.
    Case 3: Zero height.
    Case 4: Zero Width.
    Case 5: Negative p.
    Case 6: p > 1.
    """
    with pytest.raises(ValueError):
        create_maze(height, width, p)


@pytest.mark.parametrize("height, width, p",
                         [("g", 5, 0.5),
                          (1.2, 2, 0.2),
                          (10, "r", 0.4),
                          (14, 3.5, 0.8),
                          (14, 10, "t"),
                          ])
def test_illegal_dimension_inputs(height, width, p):
    """TypeError when dimensions input are wrong data type.
    Reason for TypeError in each test case.
    Case 1: Non-integer height.
    Case 2: Non-integer height.
    Case 3: Non-integer width.
    Case 4: Non-integer width.
    Case 5: Non-integer p.
    """
    with pytest.raises(TypeError):
        create_maze(height, width, p)

