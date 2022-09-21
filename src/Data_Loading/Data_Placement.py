import pandas as pd
from pathlib import Path

from src.Armor.Shield_Collection import ShieldCollection
from src.Armor.Weapon_Collection import WeaponCollection
from src.Common_general_functionalities import common_strings as cs


class DataFromLastSave:

    data_files_location = Path(__file__).parent.parent.parent.resolve() / 'Data_sets'

    def load_weapons(self):
        weapons_data = pd.read_csv(self.data_files_location / 'Weapons.csv')
        weapons_data = weapons_data.reset_index()
        weapon_data_collection = WeaponCollection(name="Hand", weight=1, material=cs.possible_materials[0], density=1, shape=cs.medium_broad + " " + cs.medium_length, efficient=False, sound="hhwee")
        for index, row in weapons_data.iterrows():
            weapon_data_collection.insert_weapon(name=row.Name, weight=float(row.Weight), material=row.Material, density=float(row.Density), shape=row.Shape, efficient=bool(row.Efficient), sound=row.Sound)
        return weapon_data_collection

    def load_shields(self):
        shields_data = pd.read_csv(self.data_files_location / 'Shields.csv')
        shields_data = shields_data.reset_index()
        shields_data_collection = ShieldCollection(name="Hand", weight=1, material=cs.possible_materials[0], density=1, shape=cs.medium_broad + " " + cs.medium_length, efficient=False, sound="hhwee")
        for index, row in shields_data.iterrows():
            shields_data_collection.insert_shield(name=row.Name, weight=float(row.Weight), material=row.Material, density=float(row.Density), shape=row.Shape, efficient=bool(row.Efficient), sound=row.Sound)
        return shields_data_collection

    def get_armor_data(self):
        return {"Weapons": self.load_weapons(), "Shields": self.load_shields()}
