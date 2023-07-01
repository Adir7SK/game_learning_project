import random

from src.Data_Loading.Data_Placement import DataFromLastSave
from src.Data_Loading.Last_Save import LastSave

from src.Characters.Main_Character import MainCharacter

from src.Intermediate.Universe_Construction import Universe
from src.Field.PlanetConditions import planets
from src.Final.Movable_Actions import Move


if __name__ == "__main__":
    general_data = DataFromLastSave().get_armor_data('Shields_Copy.csv', 'Weapons_Copy.csv')
    save_level, weapon_id, shield_id, save_life = LastSave().load()
    save_level = int(save_level)
    weapon_id = int(weapon_id)
    shield_id = int(shield_id)
    save_life = int(save_life)
    player = MainCharacter(save_life, 0, 0, general_data["Weapons"].search(weapon_id), general_data["Shields"].search(shield_id))
    vertical = random.choice(range(8, 1 + min(12, save_level * 10)))
    horizontal = random.choice(range(8, 1 + min(12, save_level * 10)))
    place = random.choice(list(planets.keys()))
    u = Universe(vertical, horizontal, place, save_level)
    b, e, a = u._initialize_field()
    program = Move(u, player, b, e, a, save_level, general_data)

    while True:
        u.print_field()
        next_step = input("Next move: ")
        program.step(next_step)
        program.fight_update()


"""
Notice!! Before closing it down, we did not commit and upload all the dummy changes (that are not working correctly)
and that were done quickly without testing/good testing just so there will be some game to run. The modules that
you must go through, change/upgrade/add testing/improve testings are: Movable_Actions, Data_Placement,
Last_Save, Live_Actions.

Notice also that we used to have the folder containing this entire project on the desktup, and now we moved it to be
in some folder instead! maybe this can create some problems. If you delete this text, then the program should run,
but ater a bit there should come errors (sometimes errors come immediately, then just run again, and it should be fine).
If this does not work, then move the entire projects folder back to the desktop.

Note that it's impossible to add another item with the same serial number as an item that is already in the items bag
"""
