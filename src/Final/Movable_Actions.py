from src.Intermediate.Assigning_Characters import Assignments
from src.Final.Fight_Handle import Fight
import src.Common_general_functionalities.common_strings as cs


class Move:

    """
    This class needs the field, the results from the initialization method of the field (not init), the main player
    object, level, and the data tree.
    This class gives the option to move and add aid to the item bag. It also updates the field, corresponding to
    fight results.
    """

    def __init__(self, field, player, level, data_tree):
        self.field = field
        self.mapping = Assignments(field, level, data_tree)
        self.player = player
        self.extra_helper_characters = []

    def step(self, move_s):
        move_string = move_s.upper()
        direction_to_numerics = {cs.directions[0]: (-1, 0), cs.directions[1]: (1, 0), cs.directions[2]: (0, 1),
                                 cs.directions[3]: (0, -1)}
        all_directions = cs.directions[0] + cs.directions[1] + cs.directions[2] + cs.directions[3]
        move_type = list(s for s in cs.multi_step if move_string.startswith(s))
        rep = None
        direction = None
        if move_type and 0 < int(move_string[len(move_type[0])]) < 99999 and \
                (move_string[len(move_type[0])+2:] in all_directions or move_string[len(move_type[0])+3:] in
                 all_directions):
            if move_string[len(move_type[0])+2:] in all_directions:
                rep = int(move_string[len(move_type[0])])   ### Must check what if we get an input such as "gy north" this should be illegal contrary to "g5 north" or "go north"
                direction = cs.directions[0] if move_string[len(move_type[0])+2:] in cs.directions[0] else \
                    (cs.directions[1] if move_string[len(move_type[1])+2:] in cs.directions[1] else
                     (cs.directions[2] if move_string[len(move_type[2])+2:] in cs.directions[2] else
                      (cs.directions[3] if move_string[len(move_type[3])+2:] in cs.directions[3] else None)))
            else:
                rep = int(move_string[len(move_type[0]):len(move_type[0])+1])
                direction = cs.directions[0] if move_string[len(move_type[0])+3:] in cs.directions[0] else \
                    (cs.directions[1] if move_string[len(move_type[1])+3:] in cs.directions[1] else
                     (cs.directions[2] if move_string[len(move_type[2])+3:] in cs.directions[2] else
                      (cs.directions[3] if move_string[len(move_type[3])+3:] in cs.directions[3] else None)))
        elif list(s for s in cs.one_step if move_string.startswith(s)) and \
                move_string[list(s for s in cs.one_step if move_string.startswith(s))[0]:] in all_directions:
            d = move_string[list(s for s in cs.one_step if move_string.startswith(s))[0]:]
            direction = cs.directions[0] if d in cs.directions[0] else (cs.directions[1] if d in cs.directions[1] else
                                                                        (cs.directions[2] if d in cs.directions[2] else
                                                                        (cs.directions[3] if d in cs.directions[3] else
                                                                         None)))
            rep = 1
        elif any(move_string.startswith(s) for s in cs.use_aid):
            ul = len(list(move_string.startswith(s) for s in cs.use_aid)[0])
            self.player.use_aid(move_string[ul:])
        elif any(move_string.startswith(s) for s in cs.info):
            il = len(list(move_string.startswith(s) for s in cs.info)[0])
            if move_string[il:] in cs.specific_info:
                if move_string[il:] == cs.character or move_string[il:] == cs.me:
                    self.player.character_info()
                if move_string[il:] == cs.helper:
                    print([[p.life, p.weapon.serial_number(), p.shield.serial_number()]
                           for p in self.extra_helper_characters])
                if move_string[il:] == cs.weapon:
                    self.player.weapon_info()
                if move_string[il:] == cs.shield:
                    self.player.shield_info()
                if move_string[il:] == cs.aids:
                    self.player.items()
                if move_string[il:] == cs.short_info:
                    self.player.short_armor_info()
        else:
            print("Invalid Command")
            return True
        if rep is not None:
            game_continues = True
            for _ in range(rep):
                if not self.player.energy:
                    if cs.energy not in [name for (name, s_id) in self.player.items()]:
                        self.player.renew_energy()
                        self.player.energy = (True, 70*5)
                        print("Character has no energy - small refill of energy granted!")
                    else:
                        print("No energy left - use your {} to refill!".format(cs.energy))
                    break
                self.player.energy = (True, self.field.energy_spent_per_step())
                self.field.update_field(direction_to_numerics[direction])
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
                fight = Fight(self.player, self.mapping.get_enemy(in_fight), self.extra_helper_characters)
            else:
                fight = Fight(self.player, self.mapping.boss, self.extra_helper_characters)
            while fight.fight_ongoing():
                """
                Here it should be clearly expressed the fight scene. At the moment it is very dumb.
                In the future, there should be a count down, that gives the player time to defend with shield.
                Right now it automatically defends.
                """
                potential_next_move = input("What are you going to do next: ").upper()
                if any(potential_next_move.startswith(s) for s in cs.use_aid):
                    ul = len(list(potential_next_move.startswith(s) for s in cs.use_aid)[0])
                    pl = fight.main_character
                    pl.use_aid(potential_next_move[ul:])
                    fight.update_players(pl)
                elif potential_next_move in cs.fight_actions[:2]:
                    fight.player_is_hitting()
                elif potential_next_move in cs.fight_actions[2:]:
                    print("Currently there is no use for this function.")
                fight.enemy_is_hitting()

            if fight.main_character.alive and not fight.enemy.alive:
                self.mapping.remove_enemy(self.field.main_character_position)
                self.player = fight.main_character
                self.field.update_after_fight_victory()
                print("You won the fight!")
                return True
            elif not fight.main_character.alive and fight.enemy.alive:
                print("You lost the fight :( Game Over!")
                return False
        else:
            return True

#### HERE WE SAW THAT THE WAY OF USING AND AID IS TYPING "use AID_SERIAL_NUMBER"
#### WE ALSO SAW THAT MOVING IS WITH TYPING EITHER "GO NORTH/SOUTH/EAST/WEST" OR "G5 NORTH/..." THEN IT TAKES 5 STEPS
#### WE ALSO SEE THAT THE WAY TO ATTACK AND DEFEND IS SIMPLY BY TYPING ATTACK AND DEFEND RESPECTIVELY
#### The way it should work: this class is initiated at the beginning of each level, and the method step is called
####    in a loop until either the boss is defeated (and level is completed) or game is over. This class takes care for
####    collecting items, update the field after every action, and starting and handeling a fight

"""
Tests:

Universe_Construction:
Edit the if __main__ at the end

Fight_Handle and this (Movable_Actions):
Test everything because we have no test
"""
