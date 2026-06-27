import pandas as pd
import matplotlib.pyplot as plt
import sqlite3

def main():
    df = load_data('data/pokemon.csv', 'pokemon')
    print(df)

def load_data(file_name, table_name):
    conn = sqlite3.connect('data/data.db')

    df = pd.read_csv(file_name)
    df.to_sql(table_name, conn, if_exists='replace', index=False)

    conn.close()

    return df

def clean_data():
    ...

if __name__ == "__main__":
    main()