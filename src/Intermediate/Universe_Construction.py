from src.Field.Improved_Maze_Generator import Maze
from src.Field.PlanetConditions import planets
import src.Common_general_functionalities.common_strings as cs

import random
import operator
from colorama import init, Fore


class Universe(Maze):
    """
    This class creates and accommodate the universe/field/maze suitable to the level the player is at.
    Upon initialization, we insert the field's dimensions, planet, and level.
    _initialize_field - initialize field from start to end with all the characteristics of that level. This method
                        should not be called, except within this class. This is called only within field attribute below
    legal_to_move - returns all the legal moves from player's current position.
    update_field - given a move, this method will update the field (i.e. the player's new position).
    update_after_fight_victory - used after winning a fight with some enemy, the field and corresponding symbols will
                                 be updated.
    print_field - colour coded printed field adjusted to every character on the board.
    field, energy_spent_per_step, main_character_position - are serving as attributes and are self-explanatory by name.
    """
    def __init__(self, dim_y, dim_x, planet, level):
        if not isinstance(level, int) or level < 1:
            raise AttributeError("The level must be a positive integer!")
        self.level = level
        super().__init__(dim_y, dim_x, time_limit=level)
        if type(planet) != str or planet.lower() not in planets.keys():
            raise AttributeError("This planet does not exist.")
        self._planet = planets[planet.lower()]
        self._field = []
        self._main_character_position = (0, 0)

    @property
    def field(self):
        if not self._field:
            self._initialize_field()
        return self._field

    @field.setter
    def field(self, value):
        raise AttributeError("It is impossible to manually update/set the field. You must update it through moves.")

    @field.deleter
    def field(self):
        raise AttributeError("It is impossible to delete the field!")

    def _initialize_field(self):
        """
        Here we initialize the field given the level.
        Field initialization includes changing the cells value of the printed field, to symbolize the positions of
        characters, enemies, boss, and aid kits.
        It returns one tuple and two arrays of tuples which are respectively indicating the position of Boss,
        Enemies, and Aid kits.

        Still missing: dealing with more types of enemies, adding helper characters, adding undercover characters.

        Currently, the number of aids and enemies is the same as the level.
        """
        maze = super().generate_maze()
        boss_position = [(row, col) for row, row_vals in enumerate(maze) for col, cell_val in enumerate(row_vals) if
                         cell_val == 2][0]
        potential_enemies_positions = [(row, col) for row, row_vals in enumerate(maze) for col, cell_val in
                                       enumerate(row_vals) if cell_val == 1]
        enemies_positions = []
        for _ in range(self.level):
            location = random.choice(potential_enemies_positions)
            if location != (0, 0):
                enemies_positions.append(location)
        potential_aid_positions = [(row, col) for row, row_vals in enumerate(maze) for col, cell_val in
                                   enumerate(row_vals) if cell_val == 3]
        if not potential_aid_positions:
            potential_aid_positions = list(filter(lambda i: i not in enemies_positions, potential_enemies_positions))
        aid_positions = []
        for _ in range(self.level):
            location = random.choice(potential_aid_positions)
            if location != (0, 0):
                aid_positions.append(location)
        del potential_enemies_positions, potential_aid_positions
        # From here we start replacing the numbers with the symbols of the game's different characters
        maze[boss_position[0]][boss_position[1]] = cs.boss
        for location in enemies_positions:
            maze[location[0]][location[1]] = cs.regular_enemy
        for location in aid_positions:
            maze[location[0]][location[1]] = cs.aid
        maze[self.main_character_position[0]][self.main_character_position[1]] = cs.main_character
        for row in range(len(maze)):
            for col in range(len(maze[0])):
                if maze[row][col] == 0:
                    maze[row][col] = cs.no_path
                elif maze[row][col] in [1, 3]:
                    maze[row][col] = cs.path
        self._field = maze
        # return boss_position, enemies_positions, aid_positions

    @property
    def energy_spent_per_step(self):
        return self._planet.gravity / 10

    @energy_spent_per_step.setter
    def energy_spent_per_step(self, val):
        raise AttributeError("Energy spent per step depends on plant's gravity and can not be changed!")

    @energy_spent_per_step.deleter
    def energy_spent_per_step(self):
        raise AttributeError("In every planet energy will be used for each step, therefore cannot be deleted.")
    
    @property
    def main_character_position(self):
        return self._main_character_position

    @main_character_position.setter
    def main_character_position(self, new_position):
        self._main_character_position = new_position

    @main_character_position.deleter
    def main_character_position(self):
        raise AttributeError("It is impossible to remove the main character from the field.")

    def legal_moves(self):
        """
        This method returns all the legal moves that are allowed to do from main character's current position.
        """
        if self._field[self.main_character_position[0]][self.main_character_position[1]] == cs.fight:
            return []

        def legal_position(g):
            """
            This is a function factory, which returns a function that is tailored to the size of the given grid,
            and returns False if a position is out of boundaries.
            """
            def positions(p):
                if 0 <= p[0] < self.dim_x and 0 <= p[1] < self.dim_y and g[p[0]][p[1]] != cs.no_path:
                    return True
                else:
                    return False
            return positions

        possible_moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        adjusted_legal_position_checker = legal_position(self._field)
        legal_moves = []
        for pm in possible_moves:
            potential_allowed_position = tuple(map(operator.add, self.main_character_position, pm))
            if adjusted_legal_position_checker(potential_allowed_position):
                legal_moves.append(pm)
        return legal_moves

    def update_field(self, move):
        """
        This method updates the location of the main character given the move.
        If the move was allowed, this method will return True, otherwise it'll return False.
        """
        if type(move) != tuple or len(move) != 2 or move[0] not in [-1, 0, 1] or move[1] not in [-1, 0, 1]:
            raise AssertionError("Illegal move. Move must be a tuple of two integers: -1, 0, or 1.")
        if not self.legal_moves() or move not in self.legal_moves():
            print("This is an illegal move. The legal moves are: {!r}. Your position is: {!r}."
                  .format(self.legal_moves(), self.main_character_position))
            return
        previous_position = self.main_character_position
        self.main_character_position = tuple(map(operator.add, self.main_character_position, move))
        if self._field[self.main_character_position[0]][self.main_character_position[1]] in [cs.regular_enemy, cs.boss]:
            self._field[self.main_character_position[0]][self.main_character_position[1]] = cs.fight
        else:
            self._field[self.main_character_position[0]][self.main_character_position[1]] = cs.main_character
        self._field[previous_position[0]][previous_position[1]] = cs.path

    def update_after_fight_victory(self):
        self._field[self.main_character_position[0]][self.main_character_position[1]] = cs.main_character

    def print_field(self):
        init()
        for i in range(0, len(self._field)):
            for j in range(0, len(self._field[0])):
                if self._field[i][j] == cs.path:
                    print(Fore.LIGHTBLACK_EX, f'{self._field[i][j]}', end="")
                elif self._field[i][j] == cs.main_character:
                    print(Fore.YELLOW, f'{self._field[i][j]}', end="")
                elif self._field[i][j] == cs.aid:
                    print(Fore.GREEN, f'{self._field[i][j]}', end="")
                elif self._field[i][j] == cs.boss:
                    print(Fore.CYAN, f'{self._field[i][j]}', end="")
                elif self._field[i][j] == cs.regular_enemy:
                    print(Fore.BLUE, f'{self._field[i][j]}', end="")
                elif self._field[i][j] == cs.fight:
                    print(Fore.RED, f'{self._field[i][j]}', end="")
                else:
                    print(Fore.WHITE, f'{self._field[i][j]}', end="")
            print('\n')


if __name__ == "__main__":
    u = Universe(10, 10, "mArS", 5)
    b, e, a = u._initialize_field()
    u.print_field()
    while u.main_character_position != b:
        if u.field[u.main_character_position[0]][u.main_character_position[1]] == "X":
            u.update_after_fight_victory()
        i = int(input("Vertical: "))
        j = int(input("Horizontal: "))
        u.update_field((i, j))
        u.print_field()
