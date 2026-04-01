import mariadb
import json
import pandas as pd

# conn = None
# cursor = None

with open("user.json", "r") as file:
    db_config = json.load(file)


def init_mariadb():
    global conn
    global cursor

    try:
        print("Connecting to MariaDB...")
        conn = mariadb.connect(**db_config) 
        print("Connection successful!")
        cursor = conn.cursor()
    except:
        print("Connection Failed!")

def loop():
    current_operation = 1
    MD_RUN = True

    while(MD_RUN):
        print("What would you like to do:")
        print("(1) Write Record \n(2) Read Record:")
        current_operation = input()

        if (not current_operation.isdigit()):
            print("Invalid Input!\n")
            continue
        current_operation = int(current_operation)
        MD_RUN = False
    
def create_db():
    with open("./create_db.sql", 'r') as file:
        sql_script = file.read().split(";")
        sql_script.pop()

        print("\n")

        for cmd in sql_script:
            cursor.execute(cmd)
            print(f"{cmd};")

def csv_create_tables():
    input_file = "data/SpotifyFeatures.csv"

    df: pd.DataFrame = pd.read_csv(input_file)

    tracks_master = df[['track_name', 'artist_name']].drop_duplicates().copy()
    tracks_master.insert(0, 'TRACK_ID', range(1, len(tracks_master) + 1))

    tracks_master[['TRACK_ID', 'track_name']].to_csv("data/tracks_information.csv", index=False)

    df = df.merge(tracks_master, on=['track_name', 'artist_name'])

    artists_df = df[['TRACK_ID', 'artist_name']].copy()
    artists_df.insert(0, 'ARTIST_ID', range(1, len(artists_df) + 1))
    artists_df.to_csv("data/artists_information.csv", index=False)

    music_df = df[['TRACK_ID']].copy()
    music_df.insert(0, 'MUSIC_ID', range(1, len(music_df) + 1))
    music_df.to_csv("data/musicallity_information.csv", index=False)

    stats_df = df[['TRACK_ID', 'popularity', 'instrumentalness']].copy()
    stats_df.insert(0, 'STATS_ID', range(1, len(stats_df) + 1))
    stats_df.to_csv("data/statistics_information.csv", index=False)

    rhythm_df = df[['TRACK_ID']].copy()
    rhythm_df.insert(0, 'RHYTHM_ID', range(1, len(rhythm_df) + 1))
    rhythm_df.to_csv("data/rhythm_information.csv", index=False)

    tempo_df = rhythm_df[['RHYTHM_ID']].copy()
    tempo_df['tempo'] = df['tempo']
    tempo_df['time_signature'] = df['time_signature']
    tempo_df.insert(0, 'TEMPO_ID', range(1, len(tempo_df) + 1))
    tempo_df.to_csv("data/tempo_information.csv", index=False)

    prod_df = stats_df[['STATS_ID']].copy()
    prod_df['genre'] = df['genre']
    prod_df['duration_ms'] = df['duration_ms']
    prod_df.insert(0, 'PROD_ID', range(1, len(prod_df) + 1))
    prod_df.to_csv("data/production_information.csv", index=False)
    
    listen_df = stats_df[['STATS_ID']].copy()
    listen_df.insert(0, 'LISTEN_ID', range(1, len(listen_df) + 1))
    listen_df.to_csv("data/listenability_information.csv", index=False)

    loudness_df = df[["loudness","acousticness"]]
    dancebility_df = df[["danceability","liveness","valence"]]
    keys_df = df[["key","mode"]]
    loudness_df.to_csv("data/loudness_information.csv", index=False)
    dancebility_df.to_csv("data/dancebility_information.csv", index=False)
    keys_df.to_csv("data/keys_information.csv", index=False)
    

def close_mariadb():
    cursor.close()
    conn.close()

def run_db_operations():
    init_mariadb()
    create_db()
    csv_create_tables()
    close_mariadb()
    

if __name__ == "__main__":
    run_db_operations()

