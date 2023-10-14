import src.Common_general_functionalities.common_strings as cs

flexible_in_armor = ['_armor_efficiency', '_energy']
main_character_start_speed = 0.35  # Careful changing it - tests might fail
main_character_start_strength = 5  # Careful changing it - tests might fail

# Speed factor for defending
speed_factor = 10
min_weapon_strength = 398
min_shield_strength = 398
min_weapon_serial = str(min_weapon_strength)    # cs.weapon + str(min_weapon_strength)
min_shield_serial = str(min_shield_strength)
possible_weight = 500
possible_densities = 100
beginner_full_life = 50
above_absolute_max = 10e9
