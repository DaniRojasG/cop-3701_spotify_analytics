-- Create and switch to the database
CREATE DATABASE IF NOT EXISTS SpotifyAnalytics;
USE SpotifyAnalytics;

CREATE TABLE GENRES (
    Genre_Name VARCHAR(255)
    );

CREATE TABLE ARTISTS (
    Artist_ID INT PRIMARY KEY NOT NULL,
    Artist_Name VARCHAR(255)
    );

CREATE TABLE TRACKS (
    Track_ID INT PRIMARY KEY NOT NULL,
    Artist_ID INT,
    Track_Name VARCHAR(255),
    FOREIGN KEY (Artist_ID) REFERENCES ARTISTS(Artist_ID)
    );

CREATE TABLE PRODUCTION (
    Track_ID INT,
    Artist_ID INT,
    Genre_Name VARCHAR(255),
    Song_Key VARCHAR(255),
    Duration_Ms INT,
    Tempo FLOAT,
    PRIMARY KEY (Track_ID, Artist_ID),
    FOREIGN KEY (Track_ID) REFERENCES TRACKS(Track_ID),
    FOREIGN KEY (Artist_ID) REFERENCES ARTISTS(Artist_ID),
    FOREIGN KEY (Genre_Name) REFERENCES GENRES(Genre_Name)
    );

CREATE TABLE SONGATTRIBUTES (
    Track_ID INT,
    Artist_ID INT,
    Loudness FLOAT,
    Acousticness FLOAT,
    Danceability FLOAT,
    Liveliness FLOAT,
    Valence FLOAT,
    Popularity_Stat INT,
    PRIMARY KEY (Track_ID, Artist_ID),
    FOREIGN KEY (Track_ID) REFERENCES TRACKS(Track_ID),
    FOREIGN KEY (Artist_ID) REFERENCES ARTISTS(Artist_ID)
    );
