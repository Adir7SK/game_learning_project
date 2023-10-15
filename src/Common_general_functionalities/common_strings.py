offence = "Offence"
defence = "Defence"
sword = "Sword"
gun = "Gun"
body_shield = "Body Shield"
hand_shield = "Hand_shield"
root = "Root"
efficient = "Efficient"
sloppy = "Sloppy"

# Materials
wood_abaci = "Wood Abaci"
wood_african_mahogany = "Wood African Mahogany"
wood_apple = "Wood Apple"
wood_chesnut = "Wood Chesnut"
wood_cumaru = "Wood Cumaru"
wood_ebony = "Wood Ebony"
wood_hickory = "Wood Hickory"
wood_ipe = "Wood Ipe"
iron = "Iron"
inconel = "Inconel"
tungsten = "Tungsten"
titanium = "Titanium"
steel = "Steel"

possible_materials = [wood_abaci, wood_african_mahogany, wood_apple, wood_chesnut, wood_cumaru,
                      wood_ebony, wood_hickory, wood_ipe, iron, inconel, tungsten,
                      titanium, steel]

# Shape details
broad = "Broad"
medium_broad = "Medium-broad"
slim = "Slim"
long = "Long"
medium_length = "Medium-length"
short = "Short"
even = "Even"
not_even = "Not-Even"

possible_shapes = {broad: 2, medium_broad: 1, slim: 3, long: 1.8, medium_length: 1.5, short: 2.8, even: 2.9, not_even: 1.1}

# Aid types
aid_ser = "AID"
health = "Health-Kit"
energy = "Energy-Kit"
strength = "Strength-Boost"
speed = "Speed-Boost"
full_life = "Full-Life_boost"
weapon = "WEAPON"
shield = "SHIELD"
aid_types = [health, energy, strength, speed, full_life, weapon, shield]
amount_of_possible_magnitudes = 5

# Character's symbols
unknown = "?"
main_character = "@"
boss = "B"
regular_enemy = "E"
fight = "X"
aid = "H"
helper_character = 'C'
path = "O"
no_path = "|"

amount_of_possible_levels = 10  # 5

# Control commands - IF GETTING NEW COMMANDS YOU MUST CHECK THAT SUCH COMMAND DOESN'T ALREADY EXISTS FOR A DIFFERENT ACTION
one_step = ["GO ", "MOVE ", "STEP "]
multi_step = ["G", "M", "S"]
directions = [["NORTH", "UP", "N", "U"], ["SOUTH", "DOWN", "S", "D"], ["EAST", "RIGHT", "E", "R"],
              ["WEST", "LEFT", "W", "L"]]
n_loc = [i for i, d in enumerate(directions) if "NORTH" in d][0]
s_loc = [i for i, d in enumerate(directions) if "SOUTH" in d][0]
e_loc = [i for i, d in enumerate(directions) if "EAST" in d][0]
w_loc = [i for i, d in enumerate(directions) if "WEST" in d][0]
direction_to_numerics = {tuple(directions[n_loc]): (-1, 0), tuple(directions[s_loc]): (1, 0), tuple(directions[e_loc]): (0, 1),
                         tuple(directions[w_loc]): (0, -1)}
dir_map = {i: directions[j] for j in range(len(directions)) for i in directions[j]}
direction_map = lambda x: direction_to_numerics[tuple(dir_map[x])]
use_aid = ["USE ", "UTILIZE "]
attack_actions = ["ATTACK", "A"]
defend_actions = ["BLOCK", "DEFEND", "D"]
info = ["INFO ", "INFORMATION ", "TELL ME ABOUT ", "TELL ME ABOUT MY "]
character = "CHARACTER"
me = "ME"
helper = "HELPER"
aids = "AIDS"
short_info = "ARMOR"
specific_info = [character, me, helper, weapon, shield, aids, short_info]
yes = ['YES', 'Y', 'YEAH', 'JA', 'YEP', 'JEP']
no = ['NO', 'N', 'NOPE', 'NAA']

# Data tree
weapons = "WEAPONS"
shields = "SHIELDS"

# Command type
stepping = "STEPPING"
using_aid = "USE_AID"
get_information = "GET_INFORMATION"

# Inner file names and strings
weapons_csv = "Weapons.csv"
shields_csv = "Shields.csv"
game_csv = "Game_Save.csv"
data_sets = 'Data_sets'
user = 'User'
password = 'Password'
splitting_char = ';'
small_split = '^'

# Message strings (interfacing with users)
user_already_exists = "There is already a user with this name!"
user_doesnt_exist = "No such user!"
wrong_password = "Wrong Password!"
password_length_error = "Password's length must be greater than 5 characters."
double_item_error = "You cannot have twice an item with the same serial number."
serial_aid_not_there = "The serial number you typed points to an aid you currently don't have in your item collection."
drained_character = "The character has no energy to attack or defend."
energy_granted = "Character has no energy - small refill of energy granted!"
enemy_defeated = "Enemy is defeated!"
you_lose = "You are defeated!"
game_over = "GAME OVER!"
didnt_defend = "Missed your chance to defend. Please press enter to continue."
fight_start = "You are starting a FIGHT!"
fight_won = "You won the fight!"
invalid_command = "Invalid command. Please type again."
no_available_info = "You asked for information about something that we don't have information about."
new_player = "Are you a new? "
enter_user = "Please enter user: "
enter_password = "Please enter password: "
sound_question = "Would you like to play with sound? "
to_finish = "Would you like to finish the game? "
instructions = ""
