import pandas as pd
from pathlib import Path
import random

from src.Armor.Shield_Collection import ShieldCollection
from src.Armor.Weapon_Collection import WeaponCollection
from src.Common_general_functionalities import common_strings as cs


class GameDetailsData:

    data_files_location = Path(__file__).parent.parent.parent.resolve() / 'Data_sets'

    def load_weapons(self, file='Weapons.csv'):
        weapons_data = pd.read_csv(self.data_files_location / file)
        weapons_data = weapons_data.reset_index()
        weapon_data_collection = WeaponCollection(name="Hand", weight=1, material=cs.possible_materials[0], density=1, shape=cs.medium_broad + " " + cs.medium_length, efficient=False, sound="hhwee")
        for index, row in weapons_data.iterrows():
            weapon_data_collection.insert_weapon(name=row.Name, weight=float(row.Weight), material=row.Material, density=float(row.Density), shape=row.Shape, efficient=bool(row.Efficient), sound=row.Sound)
        return weapon_data_collection

    def load_shields(self, file='Shields.csv'):
        shields_data = pd.read_csv(self.data_files_location / file)
        shields_data = shields_data.reset_index()
        shields_data_collection = ShieldCollection(name="Hand", weight=1, material=cs.possible_materials[0], density=1, shape=cs.medium_broad + " " + cs.medium_length, efficient=False, sound="hhwee")
        for index, row in shields_data.iterrows():
            shields_data_collection.insert_shield(name=row.Name, weight=float(row.Weight), material=row.Material, density=float(row.Density), shape=row.Shape, efficient=bool(row.Efficient), sound=row.Sound)
        return shields_data_collection

    def get_armor_data(self, shield_file='Shields.csv', weapon_file='Weapons.csv'):
        return {cs.weapons: self.load_weapons(weapon_file), cs.shields: self.load_shields(shield_file)}

    def write_tree(self, tree, file_name):
        df_tree = tree.tree_to_df()
        df_tree.to_csv(self.data_files_location / file_name)

    def generate_data(self):
        i = 0
        weight_options = [j*0.01 for j in range(1, 500)]
        density_options = [j*0.01 for j in range(1, 100)]
        weapon_data_collection = WeaponCollection(name="Hand", weight=1, material=cs.possible_materials[0], density=1, shape=cs.medium_broad + " " + cs.medium_length, efficient=False, sound="hhwee")
        for material in cs.possible_materials:
            for s in cs.possible_shapes.keys():
                extra_s = random.choice(list(cs.possible_shapes.keys()))
                while s == extra_s:
                    extra_s = random.choice(list(cs.possible_shapes.keys()))
                shape = s + " " + extra_s
                weight = random.choice(weight_options)
                density = random.choice(density_options)
                name = "Weapon"+str(i)
                sound = "Sound"+str(i)
                weapon_data_collection.insert_weapon(name=name, weight=weight, material=material, density=density,
                                                     shape=shape, efficient=False, sound=sound)
                weapon_data_collection.insert_weapon(name=name+'e', weight=weight, material=material, density=density,
                                                     shape=shape, efficient=True, sound=sound)
                i += 1
        self.write_tree(weapon_data_collection, 'Weapons.csv')

        i = 0
        shield_data_collection = ShieldCollection(name="Hand", weight=1, material=cs.possible_materials[0], density=1,
                                                  shape=cs.medium_broad + " " + cs.medium_length, efficient=False,
                                                  sound="hhwee")
        for material in cs.possible_materials:
            for s in cs.possible_shapes.keys():
                extra_s = random.choice(list(cs.possible_shapes.keys()))
                while s == extra_s:
                    extra_s = random.choice(list(cs.possible_shapes.keys()))
                shape = s + " " + extra_s
                weight = random.choice(weight_options)
                density = random.choice(density_options)
                name = "Shield" + str(i)
                sound = "Sound" + str(i)
                shield_data_collection.insert_shield(name=name+'e', weight=weight, material=material, density=density,
                                                     shape=shape, efficient=True, sound=sound)
                shield_data_collection.insert_shield(name=name, weight=weight, material=material, density=density,
                                                     shape=shape, efficient=False, sound=sound)
                i += 1
        self.write_tree(shield_data_collection, 'Shields.csv')


if __name__ == "__main__":
    GameDetailsData().generate_data()
    a1 = GameDetailsData().get_armor_data()
    a2 = GameDetailsData().get_armor_data('Shields_Copy.csv', 'Weapons_Copy.csv')
    a1[cs.weapons].print_helper()
    print()
    print()
    print("This is the new updated data:")
    print()
    print()
    a2[cs.shields].print_helper()
