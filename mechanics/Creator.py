from Types import Type, types, gen_types
from Pokemon import Pokemon

import pandas as pd
import numpy as np

df = pd.read_csv("../data/pokemon.csv")
# print(df)


class Creator:
    def __init__(self, df):
        self.df = df

    def create_pokemon_from_number(self, dex_number, gen=6):
        entry = self.df.iloc[dex_number-1]
        name = entry["Name"]
        typing = [entry["Type_1"]]
        if (type2 := entry["Type_2"]) is not np.NaN:
            typing += [type2] 
        return Pokemon(name, typing, gen)

    def create_pokemon_from_name(self, name, gen=6):
        dex_number = self.df.loc[self.df["Name"] == name, "Number"].item()
        return self.create_pokemon_from_number(dex_number)


if __name__ == "__main__":
    creator = Creator(df)
    creator.create_pokemon_from_name("Bulbasaur")
    