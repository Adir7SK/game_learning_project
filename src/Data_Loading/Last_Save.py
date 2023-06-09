import pandas as pd
from pathlib import Path


class LastSave:

    data_files_location = Path(__file__).parent.parent.parent.resolve() / 'Data_sets'
    
    def load(self, file='Game_Save.csv'):
        data_save = pd.read_csv(self.data_files_location / file)
        data_save = data_save.reset_index()
        for index, row in data_save.iterrows():
            return row.Level, row.Weapon_ID, row.Shield_ID, row.Life
    