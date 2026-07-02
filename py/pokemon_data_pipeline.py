import pandas as pd
import sqlite3

db_path = "data/data.db"
csv_path = "data/pokemon.csv"

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
        speed
    FROM pokemon
    WHERE generation < 5
    """

# Create database
def load_data(file_name, table_name, db_path):
    # Load CSV into DB
    with sqlite3.connect(db_path) as conn:
        df = pd.read_csv(file_name)
        df.to_sql(table_name, conn, if_exists="replace", index=False)

# Clean dataset
def clean_data(db_path):
    with sqlite3.connect(db_path) as conn:
        df = pd.read_sql(query, conn)
    
    # Capitalise types
    for col in ["type1", "type2"]:
        df[col] = df[col].str.capitalize()

    return df

def main():
    load_data(csv_path, "pokemon", db_path)

    df_clean = clean_data(db_path)

    df_clean.to_json("data/pokemon.json", orient="records", indent=2)

if __name__ == "__main__":
    main()