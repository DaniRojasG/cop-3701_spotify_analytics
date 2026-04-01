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
            ("data/tracks_information.csv", "TRACKS"),
            ("data/loudness_information.csv", "LOUDNESS"),
            ("data/dancebility_information.csv", "DANCEBILITY"),
            ("data/musicallity_information.csv", "MUSICALLITY"),
            ("data/artists_information.csv", "ARTISTS"),
            ("data/rhythm_information.csv", "RHYTHM"),
            ("data/statistics_information.csv", "STATS"),
            ("data/keys_information.csv", "TRACKKEYS"),
            ("data/tempo_information.csv", "TEMPO"),
            ("data/production_information.csv", "PRODUCTION"),
            ("data/listenability_information.csv", "LISTENABILITY")
        ]

        for csv_file, table_name in tables:
            print(f"Loading {csv_file} into {table_name}...")
            df = pd.read_csv(csv_file)
            
            df.to_sql(table_name, con=engine, if_exists='append', index=False)
            print(f"Successfully loaded {table_name}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        engine.dispose()

if __name__ == "__main__":
    load_data()