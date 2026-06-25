import pandas as pd
import matplotlib.pyplot as plt
import sqlite3

# Create database
conn = sqlite3.connect('data/data.db')

# Read CSV
pokemon = pd.read_csv('data/pokemon.csv')

pd.set_option('display.max_rows', None)      # Show all rows
pd.set_option('display.max_columns', None)   # Show all columns
pd.set_option('display.width', None)         # Don't wrap columns
pd.set_option('display.max_colwidth', None)  # Show full column contents

# Create table
pokemon.to_sql('pokemon', conn, if_exists='replace', index=False)

# SQL clean dataset
query_regular = """
SELECT 
    pokedex_number,
    name,
    type1,
    type2,
    hp,
    attack,
    defense,
    sp_attack,
    sp_defense,
    speed,
    base_total,
    height_m,
    weight_kg,
    generation,
    is_legendary
FROM pokemon
WHERE generation < 5
    AND is_legendary = 0
"""

query_legendary = """
SELECT 
    pokedex_number,
    name,
    type1,
    type2,
    hp,
    attack,
    defense,
    sp_attack,
    sp_defense,
    speed,
    base_total,
    height_m,
    weight_kg,
    generation,
    is_legendary
FROM pokemon
WHERE generation < 5
    AND is_legendary = 1
"""

df_reg = pd.read_sql(query_regular, conn)
df_leg = pd.read_sql(query_legendary, conn)

# -- Regular Pokemon Graphs --

# Average Base Total Against Type
df_reg_abs = (
    df_reg
    .groupby('type1', as_index=False)['base_total']
    .mean()
    .sort_values(by='base_total', ascending=False)
)

plt.bar(
    df_reg_abs['type1'],
    df_reg_abs['base_total'],

)

plt.show()

# -- Legendary Pokemon Graphs --