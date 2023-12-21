import sqlite3

from data.config import path_to_db


def get_news(id):
    id = str(id)
    con = sqlite3.connect(path_to_db)
    cursor = con.cursor()
    res = cursor.execute(f"""SELECT * FROM Articles WHERE ID="{id}";""").fetchone()
    con.close()
    return res

def get_news_id():
    con = sqlite3.connect(path_to_db)
    cursor = con.cursor()
    res = cursor.execute(f"""SELECT ID FROM Articles;""").fetchall()
    con.close()
    return res

def add_news(news):
    con = sqlite3.connect(path_to_db)
    cursor = con.cursor()
    for n in news.itertuples():
        #print(hash(n.Link), n.Link, n.Text)
        if get_news(id=hash(n.Link)) is None:
            t = n.Text.replace('"', '\'')
            cursor.execute(f"""
            INSERT INTO Articles VALUES ("{str(hash(n.Link))}", "{n.Keywords}", "{n.Link}", "{t}");
    """)
            con.commit()
    con.close()


def get_all_news():
    con = sqlite3.connect(path_to_db)
    cursor = con.cursor()
    res = cursor.execute(f"""SELECT * FROM Articles;""").fetchall()
    con.close()
    return res


def get_all_users():
    con = sqlite3.connect(path_to_db)
    cursor = con.cursor()
    res = cursor.execute(f"""SELECT * FROM Users;""").fetchall()
    con.close()
    return res


def add_user_keywords(id, new_keywords):
    con = sqlite3.connect(path_to_db)
    cursor = con.cursor()
    keywords = cursor.execute(f"""SELECT Keywords FROM Users WHERE ID={id};""").fetchone()[0]
    keywords += ' ' + new_keywords
    res = cursor.execute(f"""UPDATE Users SET Keywords = "{keywords}" WHERE ID={id};""")
    con.commit()
    con.close()
    return res


def add_user(id):
    con = sqlite3.connect(path_to_db)
    cursor = con.cursor()
    try:
        cursor.execute(f"""INSERT INTO Users VALUES ("{id}", "");""")
        con.commit()
    except:
        pass
    con.close()
