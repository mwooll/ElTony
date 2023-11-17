from Types import types
from Pokemon import Pokemon

import pandas as pd

df = pd.DataFrame(index = types)

for element in types:
    monster = Pokemon("name", [element])
    df[element] = monster.def_table.values()

print(df)
name = "type_chart.csv"
df.to_csv(name)

file = pd.read_csv(name)
if __name__ == "__main__":
    pass