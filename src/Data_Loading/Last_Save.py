import pandas as pd
from pathlib import Path
import math
import src.Common_general_functionalities.Flexible_Attributes as fa
import src.Common_general_functionalities.common_strings as cs
from src.Characters.Main_Character import MainCharacter
from src.Characters.Good_Character import GoodCharacter
from src.Armor.Aid import Aid


class LastSave:

    data_files_location = Path(__file__).parent.parent.parent.resolve() / cs.data_sets
    
    def __init__(self):
        self.data = self._load()
        self.user = ""

    def _load(self, file=cs.game_csv):
        # data_save = pd.read_csv(self.data_files_location / file)
        # return data_save.reset_index()
        return pd.read_csv(self.data_files_location / file)

    def get_players_last_save(self, user, password, armor_tree):
        """
        The rows in the data are as follows:
        level, weapon_id, shield_id, life, full_life = int(row[2]), row[3], row[4], float(row[5]), float(row[6])
        aids, help_characters = row[7].split(cs.splitting_char), [t.split(cs.small_split) for t in row[8].split(cs.splitting_char)]
        strength, speed, dim_x, dim_y = float(row[9]), float(row[10]), int(row[11]), int(row[12])
        each element in help_characters is such list: [life, full_life, weapon_id, shield_id]
        returns level (int), main_character as was saved last time, list of helper_characters, dim_x, dim_y
        """
        if not len(self.data[self.data[cs.user] == user]):
            print(cs.user_doesnt_exist)
            return False
        relevant_df = self.data[self.data[cs.user] == user]
        relevant_df = relevant_df[relevant_df[cs.password] == password]
        if len(relevant_df) == 0:
            print(cs.wrong_password)
            return False
        if len(relevant_df) > 1:
            ValueError("There is more than one user with this User name and Password!")
        self.user = user
        row = relevant_df.iloc[0][1:]
        helpers = [] if math.isnan(row[8]) else [t.split(cs.small_split) for t in row[8].split(cs.splitting_char)]
        good_characters = []
        for h in helpers:
            g = GoodCharacter(float(h[1]), [h[2], h[3]])
            g.life = float(h[1]) - float(h[0])
            good_characters.append(g)
        aids = [] if math.isnan(row[7]) else [t.split(cs.small_split) for t in row[8].split(cs.splitting_char)]
        a = []
        for h in aids:
            a.append(Aid(float(h[1]), h[2], h[3]))
        w, s = armor_tree[cs.weapons].search(int(row[3])), armor_tree[cs.shields].search(int(row[4]))
        m = MainCharacter(float(row[6]), w, s, *a)
        m.life = float(row[6]) - float(row[5])
        m.strength = float(row[9]) - fa.main_character_start_strength
        m.speed = float(row[10]) - fa.main_character_start_speed
        return int(row[2]), m, good_characters, int(row[11]), int(row[12])

    def add_user(self, user, password, file=cs.game_csv):
        if len(self.data[self.data[cs.user] == user]):
            print(cs.user_already_exists)
            return False
        if len(password) < 6:
            print(cs.password_length_error)
            return False
        self.user = user
        self.data.loc[len(self.data.index)] = [user, password, 1, fa.min_weapon_serial, fa.min_shield_serial,
                                               fa.beginner_full_life, fa.beginner_full_life, None, None,
                                               fa.main_character_start_strength, fa.main_character_start_speed,
                                               10, 10]
        self.data.to_csv(self.data_files_location / file)
        return True

    def save(self, level, weapon_id, shield_id, life, full_life, aids, help_characters, strength, speed, dim_x, dim_y,
             file=cs.game_csv):
        """ level as int, weapon and shield serial number (string), life and full_life (float/int), aids list of tuples
        (each tuple has name, type, and magnitude), help_characters list of tuples where each tuple has [life,
        full_life, weapon_id, shield_id]"""
        new = []
        for p in help_characters:
            new.append(cs.small_split.join(p))
        aids_save = []
        for a in aids:
            aids_save.append(cs.small_split.join([a.name]+a.activate()))
        password = self.data.loc[self.data[cs.user] == self.user][cs.password]
        self.data.loc[self.data[cs.user] == self.user] = [[self.user, password, level, weapon_id, shield_id, life,
                                                           full_life, cs.splitting_char.join(aids_save),
                                                           cs.splitting_char.join(new), strength, speed, dim_x, dim_y]]
        self.data.to_csv(self.data_files_location / file)
    