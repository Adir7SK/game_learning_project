from src.Data_Loading.Data_Placement import GameDetailsData
import src.Common_general_functionalities.common_strings as cs

flexible_in_armor = ['_armor_efficiency', '_energy']
main_character_start_speed = 0.35  # Careful changing it - tests might fail
main_character_start_strength = 5  # Careful changing it - tests might fail

# Speed factor for defending
speed_factor = 10
min_weapon_strength = GameDetailsData().load_weapons().worst_weapon().search(int(GameDetailsData().load_weapons().worst_weapon()[len(cs.weapon):])).strength()
min_shield_strength = GameDetailsData().load_shields().worst_shield().search(int(GameDetailsData().load_shields().worst_shield()[len(cs.shield):])).strength()
min_weapon_serial = cs.weapons + str(GameDetailsData().load_weapons().worst_weapon())
min_shield_serial = cs.shield + str(GameDetailsData().load_shields().worst_shield())
possible_weight = 500
possible_densities = 100
beginner_full_life = 50
