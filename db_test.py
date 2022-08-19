from flask import *
import sqlite3

connection = sqlite3.connect('database.db')
print("New Connection Successful")

cursor = connection.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS Games (name text, release_year integer, age_rating integer, score float, developer text, description text)")

# game_list = [
#     ("Borderlands", 2009, 18, 90, "Gearbox Software", "Borderlands is an open shooter game with lots of loot"),
#     ("Fortnite", 2017, 12, 70, "Epic Games", "Building game with lots of players"),
#     ("Call of Duty 4: Modern Warfare", 2007, 15, 80, "Activision", "Modern Warfare is a first-person shooter game"),
# ]

# connection.executemany("INSERT INTO Games (name, release_year, age_rating, score, developer, description) VALUES (?,?,?,?,?,?)", game_list)

# connection.execute('CREATE TABLE Users (ID INT PRIMARY KEY AUTOINCREMENT NOT NULL,\
#                     Username TEXT NOT NULL,\
#                     Password TEXT NOT NULL)')
# print("Table Created Successfully")

# connection.execute('INSERT INTO Users (USERNAME, PASSWORD)\
#                     VALUES ("Sam_Conneely", "test_password")')
# connection.execute('INSERT INTO Users (USERNAME, PASSWORD)\
#                     VALUES ("Test_Username", "test_password2")')

# print("Records Created Successfully")

# cursor = connection.execute('SELECT * FROM users')

for row in cursor.execute("SELECT * FROM Games"):
    print("Name =", row[0])
    print("Release Year =", row[1])
    print("Age Rating =", row[2])
    print("Score =", row[3])
    print("Developer =", row[4])
    print("Description =", row[5])
    print("\n")

# print("Select Operation Successful")


connection.close()