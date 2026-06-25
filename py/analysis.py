import pandas as pd
import sqlite3

# Create database
conn = sqlite3.connect('data/data.db')

# Read CSVs
pokemon = pd.read_csv('data/pokemon.csv')
pokedex = pd.read_csv('data/pokedex.csv')

pd.set_option('display.max_rows', None)      # Show all rows
pd.set_option('display.max_columns', None)   # Show all columns
pd.set_option('display.width', None)         # Don't wrap columns
pd.set_option('display.max_colwidth', None)  # Show full column contents

# Create tables
pokemon.to_sql('pokemon', conn, if_exists='replace', index=False)
pokedex.to_sql('pokedex', conn, if_exists='replace', index=False)

# SQL merge + clean dataset
query = """
SELECT *
FROM pokemon
WHERE Generation < 5
    AND Name NOT LIKE '%Mega%'
    AND Name NOT LIKE '%Primal%'
"""
df_clean = pd.read_sql(query, conn)

print(df_clean)