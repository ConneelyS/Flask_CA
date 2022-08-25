from flask import render_template, url_for, request, g, flash, redirect
from game_store import app
from game_store.forms import RegistrationForm, LoginForm
from game_store.models import User, Game

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/new_game_added')
def game_added():
    return render_template('new_game_added.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f"Acount created for {form.username.data}")
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='Login', form=form)

# @app.route('/add_new_game', methods=['POST', 'GET'])
# def add():
#     message = "message"
#     if request.method == 'POST':
#         try:
#             name = request.form['new_game_name']
#             release_year = request.form['release_year']
#             age_rating = request.form['age_rating']
#             score = request.form['score_rating']
#             developer = request.form['developer']
#             description = request.form['description']
#             with sqlite3.connect("database.db") as connection:
#                 cursor = connection.cursor()
#                 cursor.execute("INSERT INTO Game (name, release_year, age_rating, score, developer, description) VALUES (?,?,?,?,?,?)", (name, release_year, age_rating, score, developer, description))
#                 connection.commit()
#                 message = "New Game Added Successfully"
#         except:
#             connection.rollback()
#             message = "Insert Statement Failed, Rollback Complete"
#         finally:
#             connection.close()
#             return render_template('add_new_game.html.', message = message)
#     return render_template('add_new_game.html.', message = message)

# @app.route('/view_games')
# def view_all_games():
#     connection = sqlite3.connect("database.db")
#     connection.row_factory = sqlite3.Row
#     cursor = connection.cursor()
#     cursor.execute("SELECT * FROM Game")
#     rows = cursor.fetchall()
#     return render_template('games_list.html', rows = rows)

# @app.route('/test_view_games')
# def test_view_games():
#     connection = sqlite3.connect("database.db")
#     connection.row_factory = sqlite3.Row
#     cur = connection.cursor()
#     cur.execute("SELECT * FROM Game")
#     rows = cur.fetchall()
#     return render_template("test_view_games.html", rows = rows)


# def get_database():
#     database = getattr(g, 'database', None)
#     # if database is None:
#     database = g.database = sqlite3.connect('database.db')
#     cursor = database.cursor()
#     cursor.execute("SELECT * FROM Game")
#     all_games = cursor.fetchall()
#     return all_games

# @app.teardown_appcontext
# def close_connection(exception):
#     database = getattr(g, 'database', None)
#     if database is not None:
#         database.close()
