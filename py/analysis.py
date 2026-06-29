import pandas as pd
import matplotlib.pyplot as plt
import sqlite3

type_colours = {
    'Normal': '#A8A77A',
	'Fire': '#EE8130',
	'Water': '#6390F0',
	'Electric': '#F7D02C',
	'Grass': '#7AC74C',
	'Ice': '#96D9D6',
	'Fighting': '#C22E28',
	'Poison': '#A33EA1',
	'Ground': '#E2BF65',
	'Flying': '#A98FF3',
	'Psychic': '#F95587',
	'Bug': '#A6B91A',
	'Rock': '#B6A136',
	'Ghost': '#735797',
	'Dragon': '#6F35FC',
	'Dark': '#705746',
	'Steel': '#B7B7CE',
	'Fairy': '#D685AD',
}

# Create database
def load_data(file_name, table_name):
    # Load CSV into DB
    with sqlite3.connect('data/data.db') as conn:
        df = pd.read_csv(file_name)
        df.to_sql(table_name, conn, if_exists='replace', index=False)

# Clean dataset
def clean_data(is_legendary):
    query = """
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
        AND is_legendary = ?
    """

    with sqlite3.connect('data/data.db') as conn:
        df = pd.read_sql(query, conn, params=(is_legendary,))
    
    # Capitalise types
    df['type1'] = df['type1'].str.capitalize()
    df['type2'] = df['type2'].str.capitalize()

    return df

# Average Base Total vs Type
def avb_by_type(df):
    # Combine types
    df_type = df.melt(
        id_vars=['name', 'base_total'],
        value_vars=['type1', 'type2'],
        value_name='type'
    )

    # Create Average Base Total
    df_abs = (
        df_type
        .groupby(['type'], as_index=False)['base_total']
        .mean()
        .sort_values(by='base_total', ascending=False)
        )
    
    # Assign colours
    colors = df_abs['type'].map(type_colours)

    plt.bar(
        df_abs['type'],
        df_abs['base_total'],
        color=colors
    )

    plt.ylabel('Average Base Total', labelpad=20)
    plt.xlabel('Type', labelpad=20)
    plt.xticks(rotation=45, ha='right')

    plt.tight_layout()
    plt.show()

def main():
    load_data('data/pokemon.csv', 'pokemon')

    regular = clean_data(0)
    legendary = clean_data(1)

    avb_by_type(regular)

if __name__ == "__main__":
    main()