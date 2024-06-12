import random

from src.Data_Loading.Data_Placement import GameDetailsData
from src.Data_Loading.Last_Save import LastSave

from src.Intermediate.Universe_Construction import Universe
from src.Field.PlanetConditions import planets
from src.Final.Movable_Actions import Move
import src.Common_general_functionalities.common_strings as cs


def play_level(level, last_dim, data_tree, main_character, helpers, last_strongest_arm, last_weakest_arm, sound):
    """
    Handles the entire level. Outside must keep track of the level, all data (reading, writing, updating), recieving sound input
    """
    last_dim = (10, 10) if last_dim == (0, 0) and level == 1 else last_dim
    planet_selection = planets.keys()
    planet_selection = list(planet_selection) if len(planet_selection) < level else list(planet_selection)[:level]
    level_planet = random.choice(planet_selection)
    dim_x = random.choice(list(range(last_dim[0], last_dim[0]+level)))
    dim_y = random.choice(list(range(last_dim[1], last_dim[1]+level)))
    current_dim = (dim_x, dim_y)
    universe = Universe(dim_x, dim_y, level_planet, level)
    game = Move(universe, main_character, level, data_tree, prev_weak_arm=last_weakest_arm,
                prev_strong_arm=last_strongest_arm, print_fight_sounds=sound)
    game.extra_helper_characters = helpers
    game_continues = True
    game.field.print_field()
    while game.mapping.boss.alive and game_continues:
        game_continues = game.step(input().upper())
        if game.print_field_str:
            game.field.print_field()
    if game.mapping.boss.alive and not game_continues:
        return False
    best_weapons = (game.mapping.boss.weapon.serial_number_int(), game.mapping.boss.shield.serial_number_int())
    return current_dim, data_tree, game.player, game.extra_helper_characters, best_weapons, \
           game.mapping.worst_enemy_weapons()


def get_data(save_object):
    res = input(cs.new_player).upper()
    while res not in cs.yes and res not in cs.no:
        res = input(cs.new_player).upper()
    user = input(cs.enter_user)
    password = input(cs.enter_password)
    if res in cs.yes:
        player_is_added = False
        while not player_is_added:
            player_is_added = save_object.add_user(user, password)
            if not player_is_added:
                user = input(cs.enter_user)
                password = input(cs.enter_password)
    res = False
    entire_armor_tree = GameDetailsData().get_armor_data()
    while not res:
        res = save_object.get_players_last_save(user, password, entire_armor_tree)
        if not res:
            user = input(cs.enter_user)
            password = input(cs.enter_password)
    saved_level, saved_main_char, saved_helpers, saved_dim_x, saved_dim_y = res
    return entire_armor_tree, saved_level, saved_main_char, saved_helpers, saved_dim_x, saved_dim_y


if __name__ == "__main__":
    print(cs.welcome_message)
    print(cs.instructions)
    saving_obj = LastSave()
    to_delete_character = input(cs.delete_user_message)
    while to_delete_character in cs.yes:
        user = input(cs.enter_user)
        password = input(cs.enter_password)
        to_delete_character = saving_obj.delete_user(user, password)
        if not to_delete_character:
            print(cs.unseccessful_delete)
        to_delete_character = input(cs.delete_user_message)
    armor_tree, level, main_char, helpers, dim_x, dim_y = get_data(saving_obj)
    inp = input(cs.sound_question).upper()
    while inp not in cs.yes and inp not in cs.no:
        inp = input(cs.sound_question).upper()
    inp = inp in cs.yes
    game_continues = True
    strongest_arm, weakest_arm = (500, 500), (0, 0)
    while game_continues:
        game_continues = play_level(level, (dim_x, dim_y), armor_tree, main_char, helpers, strongest_arm, weakest_arm, inp)
        if game_continues:
            dim_x, dim_y = game_continues[0]
            main_char, helpers, strongest_arm, weakest_arm = game_continues[2], game_continues[3], game_continues[4], \
                                                             game_continues[5]
            level += 1
            saving_obj.save(level, main_char.weapon.serial_number_int(), main_char.shield.serial_number_int(),
                            main_char.life, main_char.full_life, list(main_char.aids.values()), helpers,
                            main_char.strength, main_char.speed, dim_x, dim_y)
            game_continues = input(cs.to_finish).upper()
            while game_continues not in cs.yes and game_continues not in cs.no:
                game_continues = input(cs.to_finish).upper()
            game_continues = game_continues in cs.no
        else:
            inp = input(cs.restart_level).upper()
            while inp not in cs.yes and inp not in cs.no:
                inp = input(cs.sound_question).upper()
            game_continues = inp in cs.yes
