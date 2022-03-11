import sqlite3

con = sqlite3.connect('VoiceAI.db')
cur = con.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS Logins_Database(
    UserID INTEGER UNIQUE,
    Username TEXT UNIQUE,
    Password TEXT UNIQUE,
    Date Created TEXT
);''')

cur.execute('''CREATE TABLE IF NOT EXISTS Names(
    UserID INTEGER UNIQUE,
    FirstName TEXT NOT NULL,
    LastName TEXT
);''')

cur.execute("SELECT Logins_Database.UserID,Logins_Database.Username, Names.FirstName, Names.LastName FROM Logins_Database LEFT OUTER JOIN Names ON Logins_Database.UserID = Names.UserID")

con.commit()

cur.execute("INSERT INTO Logins_Database VALUES()")

con.close()