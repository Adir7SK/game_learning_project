import random
import operator
import time
from colorama import init, Fore

from src.Field.PlanetConditions import planets


class Maze:

    def __init__(self, dim_x, dim_y, planet_name):
        if type(dim_x) != int or type(dim_y) != int or dim_x < 1 or dim_y < 1:
            raise AttributeError("Invalid maze dimensions.")
        self.dim_x = dim_x
        self.dim_y = dim_y
        self.planet = planets[planet_name.lower()]

    @staticmethod
    def illegal_position(dim_x, dim_y, position):
        if type(dim_x) != int or type(dim_y) != int or dim_x < 1 or dim_y < 1:
            raise AttributeError("Invalid maze dimensions.")
        if type(position) != tuple or len(position) != 2 or (
                type(position[0]) != int and type(position[1]) != int):
            raise AssertionError("Invalid position input.")
        if 0 <= position[0] < dim_x and 0 <= position[1] < dim_y:
            return False
        return True

    @staticmethod
    def in_the_neighborhood(current_position, destination_position):
        """
        Here we check if the distance between the two given points is one (True) or more (False). Including diagonal.
        """
        if type(current_position) != tuple or len(current_position) != 2 or not (
                type(current_position[0]) == int and type(current_position[1]) == int):
            raise AssertionError("Invalid position input.")
        if type(destination_position) != tuple or len(destination_position) != 2 or not (
                type(destination_position[0]) == int and type(destination_position[1]) == int):
            raise AssertionError("Invalid position input.")
        diff = tuple(map(operator.sub, current_position, destination_position))
        if abs(diff[0]) in [0, 1] and abs(diff[1]) in [0, 1]:
            return True
        return False

    def is_one_in_neighborhood(self, grid, position):
        """Here we check whether there is more than one position that leads to this point."""
        def grid_for_legal_boundaries(g):
            """
            This is a function factory, which returns a function that is tailored to the size of the given grid,
            and returns False if a position is out of boundaries.
            """
            def positions(p):
                return not self.illegal_position(len(g), len(g[0]), p)
            return positions

        def get_legal_positions(pos):
            """
            This functions goes through all the positions that are one step away from current position, and
            returns a list off all the legal positions that are one step away.
            """
            possible_moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]
            possible_positions = [tuple(map(operator.add, pos, m)) for m in possible_moves]
            legal_positions = grid_for_legal_boundaries(grid)
            return [k for k in possible_positions if legal_positions(k)]

        if sum([grid[legal_position[0]][legal_position[1]] for legal_position in get_legal_positions(position)]) == 1:
            return False
        return True

    def generate_maze(self):
        zero_grid = [[0 for _ in range(self.dim_x)] for _ in range(self.dim_y)]
        moves = {"Up": (1, 0), "Down": (-1, 0), "Right": (0, 1), "Left": (0, -1)}
        zero_grid[0][0] = 1
        winning_path = []
        start_time = time.clock()
        while sum(sum(row) for row in zero_grid) < (self.dim_x * self.dim_y)*2: # number of paths including the winning path
            pointer_position = (0, 0)
            saved_pointer_position = pointer_position
            if sum(sum(row) for row in zero_grid) == 1:                            # Here we construct the winner path which is the first path we create
                while sum(sum(row) for row in zero_grid) != 3 * max(self.dim_x, self.dim_y) - 1:    # Defines the length of the winning path
                    impass_counter = -1
                    # The while loop ensures that the next step in the path will make sense
                    while self.illegal_position(self.dim_x, self.dim_y, pointer_position) or zero_grid[pointer_position[0]][pointer_position[1]] == 1 or self.is_one_in_neighborhood(zero_grid, pointer_position):
                        impass_counter += 1
                        if impass_counter == 20:        # This means that we can not make the path longer
                            zero_grid = [[0 for _ in range(self.dim_x)] for _ in range(self.dim_y)]
                            zero_grid[0][0] = 1
                            impass_counter = -1
                            pointer_position = (0, 0)
                            saved_pointer_position = pointer_position
                        pointer_position = saved_pointer_position
                        move = random.choice(list(moves.keys()))
                        pointer_position = tuple(map(operator.add, pointer_position, moves[move]))
                    print("Path current place is: [{!r}, {!r}]".format(pointer_position[0], pointer_position[1]))
                    zero_grid[pointer_position[0]][pointer_position[1]] = 1
                    saved_pointer_position = pointer_position
                    winning_path.append(pointer_position)
                    destination = pointer_position
            else:                                        # Here we build other paths which don't lead to the destination
                this_round_start_point = random.choice(winning_path)
                pointer_position = this_round_start_point
                iter = random.choice(range(self.dim_x, self.dim_x * 2))
                l = 0
                print("Circle")
                while l < self.dim_x:
                    impass_counter = -1
                    while self.in_the_neighborhood(pointer_position, destination) or self.illegal_position(self.dim_x, self.dim_y, pointer_position) or zero_grid[pointer_position[0]][pointer_position[1]] == 1:
                        impass_counter += 1
                        if impass_counter == 20:
                            pointer_position = this_round_start_point
                            impass_counter = -1
                        move = random.choice(list(moves.keys()))
                        pointer_position = tuple(map(operator.add, pointer_position, moves[move]))
                        if self.in_the_neighborhood(pointer_position, destination):
                            pointer_position = this_round_start_point
                            impass_counter = -1
                        if time.clock() - start_time > 7:
                            zero_grid[destination[0]][destination[1]] = 2
                            print("We got here")
                            return zero_grid
                    if zero_grid[pointer_position[0]][pointer_position[1]] != 1:
                        zero_grid[pointer_position[0]][pointer_position[1]] = 3
                    l += 1

        zero_grid[destination[0]][destination[1]] = 2
        return zero_grid

    @staticmethod
    def print_maze(maze):
        # colorama needs to be initialized in order to be used
        init()
        for i in range(0, len(maze)):
            for j in range(0, len(maze[0])):
                if maze[i][j] == 0:
                    print(Fore.LIGHTBLACK_EX, f'{maze[i][j]}', end="")
                elif maze[i][j] == 1:
                    print(Fore.BLUE, f'{maze[i][j]}', end="")
                elif maze[i][j] == 3:
                    print(Fore.GREEN, f'{maze[i][j]}', end="")
                else:
                    print(Fore.RED, f'{maze[i][j]}', end="")
            print('\n')


if __name__ == "__main__":
    maze_try = Maze(15, 15, "PLUTO")
    m = maze_try.generate_maze()
    print(m)
    Maze.print_maze(m)
