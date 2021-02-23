import sqlite3

conn = sqlite3.connect('anime.db')
cursor = conn.cursor()

cursor.execute("""CREATE TABLE Anime(
                Title TEXT,
                Url TEXT
                )""")

cursor.execute("""CREATE TABLE Reviews(
                Anime_id INTEGER,
                Text TEXT,
                Score INTEGER
                )""")

conn.commit()
conn.close()
