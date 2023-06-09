from src.Intermediate.Assigning_Characters import Assignments
from src.Final.Live_Actions import Fight, use_aid
import src.Common_general_functionalities.common_strings as cs


class Move:

    """
    This class needs the field, the results from the initialization method of the field (not init), the main player
    object, level, and the data tree.
    This class gives the option to move and add aid to the item bag. It also updates the field, corresponding to
    fight results.
    """

    def __init__(self, field, player, boss_position, enemies_positions, aid_positions, level, data_tree):
        self.field = field
        self.mapping = Assignments(boss_position, enemies_positions, aid_positions, level, data_tree)
        self.player = player

    def step(self, move_string):
        direction_to_numerics = {"NORTH": (-1, 0), "SOUTH": (1, 0), "EAST": (0, 1), "WEST": (0, -1)}
        if type(move_string) != str or move_string[:3].upper() != "GO " or move_string[3:].upper() not in ["NORTH", "SOUTH", "EAST", "WEST"]:
            print("This is an illegal move!")
            return
        if move_string[3:].upper() in direction_to_numerics.keys():
            self.field.update_field(direction_to_numerics[move_string[3:].upper()])
            if self.mapping.get_aid(self.field.main_character_position):
                self.player.add_item(self.mapping.get_aid(self.field.main_character_position))
                self.mapping.remove_aid(self.field.main_character_position)

    def fight_update(self):
        in_fight = [(row, col) for row, row_vals in enumerate(self.field.field) for col, cell_val in
                    enumerate(row_vals) if cell_val == cs.fight]
        if in_fight:
            print("You are starting a FIGHT!")
            if self.mapping.get_enemy(in_fight[0]):
                fight = Fight(self.player, self.mapping.get_enemy(in_fight[0]))
            else:
                fight = Fight(self.player, self.mapping.boss)
            while fight.enemy.life > 0 and fight.main_character.life > 0:
                """
                Here it should be clearly expressed the fight scene. At the moment it is very dumb.
                In the future, there should be a count down, that gives the player time to defend with shield.
                Right now it automatically defends.
                """
                potential_next_move = input("What are you going to do next: ")
                if potential_next_move[:4].upper() == "USE ":
                    number_of_aid_in_list = int(potential_next_move[4:]) - 1
                    aid_to_use = (self.player.items())[number_of_aid_in_list]
                    self.player = use_aid(self.player, aid_to_use)
                    self.player.remove_item(aid_to_use.name(), aid_to_use.serial_number())
                    continue
                elif potential_next_move.upper() == "ATTACK":
                    fight.player_is_hitting()
                elif potential_next_move.upper() == "DEFEND":
                    print("Currently there is no use for this function.")
                fight.enemy_is_hitting()

            if fight.enemy.life == 0:
                self.mapping.remove_enemy(self.field.main_character_position)
                self.player.life = self.player.full_life - fight.main_character.life
                self.mapping.remove_enemy(self.field.main_character_position)
                self.field.update_after_fight_victory()
                print("You won the fight!")
