import pandas as pd
from pathlib import Path
import src.Common_general_functionalities.Flexible_Attributes as fa
import src.Common_general_functionalities.common_strings as cs
from src.Characters.Main_Character import MainCharacter
from src.Characters.Good_Character import GoodCharacter


class LastSave:

    data_files_location = Path(__file__).parent.parent.parent.resolve() / cs.data_sets
    
    def __init__(self):
        self.data = self._load()
        self.user = ""

    def _load(self, file=cs.game_csv):
        # data_save = pd.read_csv(self.data_files_location / file)
        # return data_save.reset_index()
        return pd.read_csv(self.data_files_location / file)

    def get_players_last_save(self, user, password):
        """
        The rows in the data are as follows:
        level, weapon_id, shield_id, life, full_life = int(row[2]), row[3], row[4], float(row[5]), float(row[6])
        aids, help_characters = row[7].split(cs.splitting_char), [t.split(cs.small_split) for t in row[8].split(cs.splitting_char)]
        strength, speed, dim_x, dim_y = float(row[9]), float(row[10]), int(row[11]), int(row[12])
        each element in help_characters is such list: [life, full_life, weapon_id, shield_id]
        returns level (int), main_character as was saved last time, list of helper_characters
        """
        if not len(self.data[self.data[cs.user] == user]):
            print(cs.user_doesnt_exist)
            return False
        relevant_df = self.data[(self.data[cs.user] == user & self.data[cs.password] == password)]
        if len(relevant_df) == 0:
            print(cs.wrong_password)
            return False
        self.user = user
        row = relevant_df.iloc[2]
        helpers = [t.split(cs.small_split) for t in row[8].split(cs.splitting_char)]
        good_characters = []
        for h in helpers:
            g = GoodCharacter(float(h[1]), [h[2], h[3]])
            g.life = float(h[1]) - float(h[0])
            good_characters.append(g)
        aids = row[7].split(cs.splitting_char)
        m = MainCharacter(float(row[6]), [row[3], row[4]]+aids)
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
        """ level as int, weapon and shield serial number (string), life and full_life (float/int), aids list of serial
        number (list of strings), help_characters list of tuples where each tuple has [life, full_life, weapon_id,
        shield_id]"""
        new = []
        for p in help_characters:
            new.append(cs.small_split.join(p))
        password = self.data.loc[self.data[cs.user] == self.user][cs.password]
        self.data.loc[self.data[cs.user] == self.user] = [[self.user, password, level, weapon_id, shield_id, life,
                                                           full_life, cs.splitting_char.join(aids),
                                                           cs.splitting_char.join(new), strength, speed, dim_x, dim_y]]
        self.data.to_csv(self.data_files_location / file)
    