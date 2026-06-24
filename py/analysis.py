import pandas as pd

pokemon = pd.read_csv('data/pokemon.csv')
pokedex = pd.read_csv('data/pokedex.csv')

pokedex = pokedex.rename(columns={'name': 'Name'})

merged_df = pokemon.merge(
    pokedex[['pokedex_number', 'Name']],
    on='Name',
    how='left'
)

df_clean = merged_df[
    (merged_df['Generation'] < 5) &
    (~merged_df['Name'].str.contains('Mega|Primal', na=False))
    ]

print(df_clean.to_string())