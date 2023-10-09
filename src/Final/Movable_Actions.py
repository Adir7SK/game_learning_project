from src.Intermediate.Assigning_Characters import Assignments
from src.Final.Fight_Handle import Fight
import src.Common_general_functionalities.common_strings as cs
import re
from src.Characters.Good_Character import GoodCharacter
from src.Intermediate.Universe_Construction import Universe


class Move:

    """
    This class needs the field, the results from the initialization method of the field (not init), the main player
    object, level, and the data tree.
    This class gives the option to move and add aid to the item bag. It also updates the field, corresponding to
    fight results.
    """

    def __init__(self, field, player, level, data_tree, prev_weak_arm=(0, 0), prev_strong_arm=(0, 0), print_fight_sounds=False):
        if type(level) != int or level < 1:
            raise TypeError("Level must be a positive integer!")
        if not isinstance(field, Universe) or not isinstance(player, GoodCharacter) or not isinstance(data_tree, dict):
            raise TypeError("Initialization of level move handler must get data types: Universe, "
                            "GoodCharacter/MainCharacter, Integer, dictionary. and 2 tuples os 2 Int elements each.")
        if not data_tree[cs.weapons] or not data_tree[cs.shields]:
            raise ValueError("The tree dictionary must have one Weapon and another Shield subtrees.")
        if len(prev_weak_arm) != 2 or type(prev_weak_arm[0]) not in [int, float] or type(prev_weak_arm[1]) \
                not in [int, float] or len(prev_strong_arm) != 2 or type(prev_strong_arm[0]) not in [int, float] \
                or type(prev_strong_arm[1]) not in [int, float]:
            raise ValueError("The previous strongest and weakest armors must come in tuples of 2 containing Int/Float.")
        self.field = field
        self.mapping = Assignments(field, level, data_tree, last_round_weakest_armor=prev_weak_arm,
                                   last_round_strongest_armor=prev_strong_arm)
        self.player = player
        self.extra_helper_characters = []
        self._print_fight_sounds = print_fight_sounds if type(print_fight_sounds) == bool else False

    def step(self, move_s):
        game_continues = True
        command_result = self._translate_commands(move_s)
        if command_result is None:
            return game_continues
        if command_result[0] == cs.use_aid:
            self.player.use_aid(command_result[1])
        elif command_result[0] == cs.get_information:
            self._print_requested_info(command_result[1])
        elif command_result[0] == cs.stepping:
            rep, direction = command_result[1], command_result[2]
            for _ in range(rep):
                if not self.player.energy:
                    if cs.energy not in [name for (name, s_id) in self.player.items()]:
                        self.player.renew_energy()
                        self.player.energy = (True, 70*5)
                        print("Character has no energy - small refill of energy granted!")
                    else:
                        print("No energy left - use your {} to refill!".format(cs.energy))
                    break
                self.player.energy = (True, self.field.energy_spent_per_step)
                self.field.update_field(direction)
                if self.mapping.get_aid(self.field.main_character_position):
                    self.player.add_item(self.mapping.get_aid(self.field.main_character_position))
                    self.mapping.remove_aid(self.field.main_character_position)
                elif self.mapping.get_helper_char(self.field.main_character_position):
                    self.extra_helper_characters.append(self.mapping.get_helper_char(self.field.main_character_position))
                    self.mapping.remove_helper_char(self.field.main_character_position)
                elif self.mapping.get_enemy(self.field.main_character_position):
                    game_continues = self._fight_update()
                    break
        return game_continues

    def _fight_update(self):
        in_fight = [(row, col) for row, row_vals in enumerate(self.field.field) for col, cell_val in
                    enumerate(row_vals) if cell_val == cs.fight]
        in_fight = in_fight[0] if in_fight else None
        if in_fight:
            print("You are starting a FIGHT!")
            if self.mapping.get_enemy(in_fight):
                fight = Fight(self.player, self.mapping.get_enemy(in_fight), print_sound=self._print_fight_sounds, *self.extra_helper_characters)
            else:
                fight = Fight(self.player, self.mapping.boss, print_sound=self._print_fight_sounds, *self.extra_helper_characters)
            while fight.fight_ongoing():
                """
                Here it should be clearly expressed the fight scene. At the moment it is very dumb.
                In the future, there should be a count down, that gives the player time to defend with shield.
                Right now it automatically defends.
                """
                type_move, action = self._translate_commands(input("Next move: ").upper(), in_fight=True)
                if type_move == cs.use_aid:
                    pl = fight.main_character
                    pl.use_aid(action)
                    fight.update_players(pl)
                elif type_move == cs.get_information:
                    self._print_requested_info(action)
                elif type_move == cs.offence:
                    fight.player_is_hitting()
                if fight.enemy.alive:
                    fight.enemy_is_hitting()

            if fight.main_character.alive and not fight.enemy.alive:
                self.mapping.remove_enemy(self.field.main_character_position)
                self.player = fight.main_character
                self.extra_helper_characters = fight.additional_good_characters
                self.field.update_after_fight_victory()
                print("You won the fight!")
                return True
            elif not fight.main_character.alive and fight.enemy.alive:
                print("You lost the fight :( Game Over!")
                return False
        else:
            return True

    @staticmethod
    def _translate_commands(command, in_fight=False):
        """
        Converts the input string the player/user types to the information we need. For example it'll check whether
        they've requested to get some information or use some aid. Another example is whether they
        """
        if type(command) != str:
            print("Invalid command. Please type again.")
            return None
        move_string = command.upper()
        if not in_fight:
            if any(move_string.startswith(s) for s in cs.use_aid):
                return cs.use_aid, move_string.split()[-1]
            elif any(move_string.startswith(s) for s in cs.info):
                if move_string.split()[-1] in cs.specific_info:
                    return cs.get_information, move_string.split()[-1]
                else:
                    print("You asked for information about something that we don't have information about.")
                    return None
            all_directions = list(cs.dir_map.keys())
            move_type_len = len(list(s for s in cs.one_step if move_string.startswith(s)))
            slow_move = True if move_type_len else False
            move_type_len = len(list(s for s in cs.multi_step if move_string.startswith(s))) if not slow_move else move_type_len
            slow_move = True if slow_move else (False if move_type_len else None)
            num_in_step = [int(s) for s in re.findall(r'\d+', move_string)]
            rep = num_in_step[0] if slow_move is not None and len(num_in_step) == 1 else 1
            if slow_move is None or len(num_in_step) > 1 or move_string.split()[-1] not in all_directions or \
                    len(move_string) > move_type_len + 3 + max([len(i) for i in all_directions]):
                print("Invalid command. Please type again.")
                return None
            direction = cs.direction_map(move_string.split()[-1])   # The input might need to be changed to tuple type
            return cs.stepping, rep, direction
        elif in_fight:
            if any(move_string.startswith(s) for s in cs.use_aid):
                return cs.use_aid, move_string.split()[-1]
            elif any(move_string.startswith(s) for s in cs.info):
                if move_string.split()[-1] in cs.specific_info:
                    return cs.get_information, move_string.split()[-1]
                else:
                    print("You asked for information about something that we don't have information about.")
                    return None
            elif move_string in cs.attack_actions:
                return cs.offence, cs.attack_actions[0]
                # Defence commands are taken care of in Fight_Handle with countdown method

    def _print_requested_info(self, request):
        if request == cs.character or request == cs.me:
            self.player.character_info()
        if request == cs.helper:
            print([[p.life, p.weapon.serial_number(), p.shield.serial_number()]
                   for p in self.extra_helper_characters])
        if request == cs.weapon:
            self.player.weapon_info()
        if request == cs.shield:
            self.player.shield_info()
        if request == cs.aids:
            self.player.items()
        if request == cs.short_info:
            self.player.short_armor_info()



#### HERE WE SAW THAT THE WAY OF USING AND AID IS TYPING "use AID_SERIAL_NUMBER"
#### WE ALSO SAW THAT MOVING IS WITH TYPING EITHER "GO NORTH/SOUTH/EAST/WEST" OR "G5 NORTH/..." THEN IT TAKES 5 STEPS
#### WE ALSO SEE THAT THE WAY TO ATTACK AND DEFEND IS SIMPLY BY TYPING ATTACK AND DEFEND RESPECTIVELY
#### The way it should work: this class is initiated at the beginning of each level, and the method step is called
####    in a loop until either the boss is defeated (and level is completed) or game is over. This class takes care for
####    collecting items, update the field after every action, and starting and handeling a fight
