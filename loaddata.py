import pandas as pd
import json
from sqlalchemy import create_engine

with open("user.json", "r") as file:
    db_config = json.load(file)

def load_data():
    try:
        print("Connecting to MariaDB via SQLAlchemy...")
        conn_str = (
            f"mariadb+mariadbconnector://{db_config['user']}:{db_config['password']}"
            f"@{db_config['host']}/{db_config['database']}"
        )
        engine = create_engine(conn_str)
        print("Connection successful!")

        tables = [
            ("data/genres.csv", "GENRES"),
            ("data/artists.csv", "ARTISTS"),
            ("data/tracks.csv", "TRACKS"),
            ("data/production.csv", "PRODUCTION"),
            ("data/songattributes.csv", "SONGATTRIBUTES")
        ]

        for csv_file, table_name in tables:
            print(f"Loading {csv_file} into {table_name}...")
            df = pd.read_csv(csv_file)
            
            df.to_sql(table_name, con=engine, if_exists='append', index=False)
            print(f"Successfully loaded {table_name}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'engine' in locals():
            engine.dispose()

if __name__ == "__main__":
    load_data()
