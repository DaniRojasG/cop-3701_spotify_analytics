import streamlit as st
import mysql.connector
import pandas as pd

# Database Configuration
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "GR3yFryJh4ln()",
    "database": "SpotifyAnalytics",
    "port": 3306,
}

# --- DATABASE CONNECTION & HELPER FUNCTION ---

@st.cache_resource
def init_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        st.error(f"Failed to connect to database: {e}")
        st.stop() # Stops the app from running further if the DB fails

sqlconn = init_connection()
cur = sqlconn.cursor()

def run_query(query, params=None):
    cur.execute(query, params)
    data = cur.fetchall()
    column_names = [col[0] for col in cur.description]
    return pd.DataFrame(data, columns=column_names)


# --- APP UI ---
st.title("Song and Artist Tracker !")

menu = ["Query1", "Query2", "Query3", "Query4", "Query5"]
choice = st.sidebar.selectbox("Select Query", menu)

# --- SQL QUERIES ---

query1 = """
SELECT t.Track_Name, s.Liveness 
FROM TRACKS t 
JOIN SONGATTRIBUTES s ON t.Track_ID = s.Track_ID 
JOIN PRODUCTION p ON t.Track_ID = p.Track_ID
WHERE s.Liveness BETWEEN -1.0 AND 1.0 
AND p.Genre_Name LIKE %s;
"""

query2 = "SELECT COUNT(Track_ID) AS Song_Count FROM SONGATTRIBUTES WHERE Danceability < %s;"

query3 = "SELECT COUNT(Artist_ID) AS Artist_Count FROM ARTISTS WHERE Artist_Name LIKE %s;"

query4 = "SELECT COUNT(Track_ID) AS Song_Count FROM PRODUCTION WHERE Song_Key = %s;"

query5 = "SELECT t.Track_Name, s.Valence FROM TRACKS t JOIN SONGATTRIBUTES s ON t.Track_ID = s.Track_ID WHERE s.Valence < %s;"


# --- QUERY MENU SELECTION ---

if choice == "Query1":
    st.subheader("See songs within a liveness range of -1.0 to 1.0 in a given genre")
    genre_input = st.text_input("Enter a Genre:")

    if st.button("Run Query"):
        if genre_input:
            try:
                df = run_query(query1, (f"%{genre_input}%",))

                if not df.empty:
                    st.write(f"Songs in the '{genre_input}' genre within the liveness range:")
                    st.dataframe(df, use_container_width=True)
                else:
                    st.warning(f"Could not find any songs matching the genre: '{genre_input}'")

            except Exception as e:
                st.error(f"Could not execute SQL query! Error: {e}")
        else:
            st.info("Please enter a genre first.")

elif choice == "Query2":
    st.subheader("See how many songs are under a specific danceability threshold")
    danceability = st.text_input("Danceability (e.g., 0.8):")

    if st.button("Run Query"):
        if danceability:
            try:
                df = run_query(query2, (float(danceability),))
                st.metric(label="Song Count:", value=df.iloc[0, 0])
            except ValueError:
                st.error("Please enter a valid number for danceability.")
            except Exception as e:
                st.error(f"Query failed: {e}")
        else:
            st.info("Please enter a threshold first.")

elif choice == "Query3":
    st.subheader("Display all artists whose name contains a specific letter/phrase")
    search_term = st.text_input("Letter or Phrase:")

    if st.button("Run Query"):
        if search_term:
            try:
                df = run_query(query3, (f"%{search_term}%",))
                if not df.empty:
                    st.metric(label=f"Artists matching '{search_term}'", value=df.iloc[0, 0])
                else:
                    st.warning("No artists found.")
            except Exception as e:
                st.error(f"Query failed: {e}")
        else:
            st.info("Please enter a search term.")

elif choice == "Query4":
    st.subheader("Select a Song Key to see how many songs use it")
    key = st.text_input("Key (e.g., F#, etc.): ")

    if st.button("Run Query"):
        if key:
            try:
                df = run_query(query4, (key,))
                if not df.empty and df.iloc[0, 0] > 0:
                    st.metric(label="Total Songs Found:", value=df.iloc[0, 0])
                else:
                    st.warning("No songs found for that key.")
            except Exception as e:
                st.error(f"Query failed: {e}")
        else:
            st.info("Please enter a key.")

elif choice == "Query5":
    st.subheader("Shows the amount of songs under a specific valence threshold")
    valence = st.text_input("Valence (e.g., 0.5): ")

    if st.button("Run Query"):
        if valence:
            try:
                df = run_query(query5, (float(valence),))
                if not df.empty:
                    st.dataframe(df, use_container_width=True)
                else:
                    st.warning("No songs found under that threshold!")
            except ValueError:
                st.error("Please enter a valid number for valence.")
            except Exception as e:
                 st.error(f"Query failed: {e}")
        else:
            st.info("Please enter a valence threshold.")
