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

    # GENRES Table
    genres_df = pd.DataFrame(df['genre'].unique(), columns=['Genre_Name'])
    genres_df.to_csv("data/genres.csv", index=False)

    # ARTISTS Table
    artists_df = pd.DataFrame(df['artist_name'].unique(), columns=['Artist_Name'])
    artists_df.insert(0, 'Artist_ID', range(1, len(artists_df) + 1))
    artists_df.to_csv("data/artists.csv", index=False)

    # Merge Artist_ID back to main df to use as a Foreign Key
    df = df.merge(artists_df, left_on='artist_name', right_on='Artist_Name')

    # TRACKS Table

    tracks_df = df[['track_name', 'Artist_ID']].drop_duplicates().reset_index(drop=True)
    tracks_df.insert(0, 'Track_ID', range(1, len(tracks_df) + 1))
    tracks_df.rename(columns={'track_name': 'Track_Name'}, inplace=True)
    tracks_df.to_csv("data/tracks.csv", index=False)


    df = df.merge(tracks_df, left_on=['track_name', 'Artist_ID'], right_on=['Track_Name', 'Artist_ID'])

    # PRODUCTION Table
    production_df = df[['Track_ID', 'Artist_ID', 'genre', 'key', 'duration_ms', 'tempo']].copy()
    production_df.rename(columns={
        'genre': 'Genre_Name',
        'key': 'Song_Key',
        'duration_ms': 'Duration_Ms',
        'tempo': 'Tempo'
    }, inplace=True)

    production_df = production_df.drop_duplicates(subset=['Track_ID', 'Artist_ID'])
    production_df.to_csv("data/production.csv", index=False)

    # SONGATTRIBUTES Table
    songattributes_df = df[['Track_ID', 'Artist_ID', 'loudness', 'acousticness', 'danceability', 'liveness', 'valence', 'popularity']].copy()
    songattributes_df.rename(columns={
        'loudness': 'Loudness',
        'acousticness': 'Acousticness',
        'danceability': 'Danceability',
        'liveness': 'Liveliness',
        'valence': 'Valence',
        'popularity': 'Popularity_Stat'
    }, inplace=True)


    songattributes_df = songattributes_df.drop_duplicates(subset=['Track_ID', 'Artist_ID'])
    songattributes_df.to_csv("data/songattributes.csv", index=False)


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
