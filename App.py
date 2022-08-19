from distutils.log import debug
from operator import ge
import sqlite3
from typing import final
from flask import Flask, render_template, request, g
app = Flask(__name__)

# posts= [
#     {
#         "name": "Borderlands",
#         "release_year": "2009",
#         "age_rating": "18",
#         "score": "90",
#         "developer": "Gearbox Software",
#         "description": "Borderlands is an open shooter game with lots of loot"
#     },

#     {
#         "name": "Fortnite",
#         "release_year": "2017",
#         "age_rating": "12",
#         "score": "70",
#         "developer": "Epic Games",
#         "description": "Building game with lots of players"
#     },

#     {
#         "name": "Borderlands 2",
#         "release_year": "2014",
#         "age_rating": "18",
#         "score": "95",
#         "developer": "Gearbox Software",
#         "description": "Borderlands 2 is an open shooter game with even more loot"
#     },

#     {
#         "name": "Call of Duty 4: Modern Warfare",
#         "release_year": "2007",
#         "age_rating": "15",
#         "score": "80",
#         "developer": "Activision",
#         "description": "Modern Warfare is a first-person shooter game"
#     }

# ]

@app.route('/')
def home():
    return render_template('home.html')

# @app.route('/games')
# def games():
#     list_of_games = get_database()
#     return str(list_of_games)
    # return render_template('games_list.html')

@app.route('/new_game_added')
def game_added():
    return render_template('new_game_added.html')

# @app.route('/login')
# def login():
#     return render_template('login.html')

@app.route('/add_new_game', methods=['POST', 'GET'])
def add():
    if request.method == 'POST':
        try:
            name = request.form['new_game_name']
            release_year = request.form['release_year']
            age_rating = request.form['age_rating']
            score = request.form['score_rating']
            developer = request.form['developer']
            description = request.form['description']
            with sqlite3.connect("database.db") as connection:
                cursor = connection.cursor()
                cursor.execute("INSERT INTO Games (name, release_year, age_rating, score, developer, description) VALUES (?,?,?,?,?,?)", (name, release_year, age_rating, score, developer, description))
                connection.commit()
                message = "New Game Added Successfully"
        except:
            connection.rollback()
            message = "Failed Insertion, Rollback Complete"
        finally:
            connection.close()
            return render_template('add_new_game.html.', message = message)
    #return render_template('add_new_game.html.', message = message)

# @app.route('/test_view_games')
# def test_view_games():
#     connection = sqlite3.connect("database.db")
#     connection.row_factory = sqlite3.Row
#     cur = connection.cursor()
#     cur.execute("SELECT * FROM Games")
#     rows = cur.fetchall()
#     return render_template("test_view_games.html", rows = rows)


# def get_database():
#     database = getattr(g, 'database', None)
#     # if database is None:
#     database = g.database = sqlite3.connect('database.db')
#     cursor = database.cursor()
#     cursor.execute("SELECT * FROM Games")
#     all_games = cursor.fetchall()
#     return all_games

# @app.teardown_appcontext
# def close_connection(exception):
#     database = getattr(g, 'database', None)
#     if database is not None:
#         database.close()

if __name__ == '__main__':
    app.run(debug = True)