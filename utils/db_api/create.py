import sqlite3


conn = sqlite3.connect('../../data/news_database.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        ID LONG PRIMARY KEY,
        Keywords TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Articles (
        ID TEXT PRIMARY KEY,
        Keywords TEXT,
        Link TEXT,
        Title TEXT
    )
''')
#print(cursor.execute('''SELECT * FROM Articles WHERE ID = "8952360084313600237"''').fetchone())
conn.commit()
conn.close()
