import sqlite3
from data_dict import random_users

def create():
    try:
        with sqlite3.connect('member.db') as conn:
            cur = conn.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS members (id INTEGER PRIMARY KEY AUTOINCREMENT, first_name TEXT, last_name TEXT, birth_date TEXT, gender TEXT, email TEXT, phonenumber TEXT, address TEXT, nationality TEXT, active INTEGER, github_username TEXT)")
            
            # Check how many members are already in the database
            cur.execute('SELECT COUNT(*) FROM members')
            count = cur.fetchone()[0]

            # If there are fewer than 10 members, insert the difference
            if count < 10:
                members_to_insert = random_users[:10 - count]  # Adjust this based on your data source
                cur.executemany('''INSERT INTO members 
                    (first_name, last_name, birth_date, gender, email, phonenumber, address, nationality, active, github_username) 
                    VALUES (:first_name, :last_name, :birth_date, :gender, :email, :phonenumber, :address, :nationality, :active, :github_username)''', members_to_insert)
            else:
                print("Database already has 10 members.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")


def data():
    members = []
    with sqlite3.connect('member.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT * FROM members')
        rows = cur.fetchall()

        for row in rows:
            members.append({
                'id': row[0],
                'first_name': row[1],
                'last_name': row[2],
                'birth_date': row[3],
                'gender': row[4],
                'email': row[5],
                'phonenumber': row[6],
                'address': row[7],
                'nationality': row[8],
                'active': row[9],
                'github_username': row[10]
            })

    return members