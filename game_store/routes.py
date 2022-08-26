from flask import render_template, url_for, request, g, flash, redirect
from flask_login import login_user, current_user, logout_user, login_required
from game_store import app, db, bcrypt
from game_store.forms import RegistrationForm, LoginForm, UpdateGameForm
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
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("Account created, you are able to log in", 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash("Login Unsucessful. Please check email and password", 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/game')
@login_required
def game():
    form = UpdateGameForm()
    game_details = Game.query.first()
    # Later fix the images for each specific game within the databse Game(game.game_iamge) table
    game_image = url_for('static', filename='game_images/' + 'default.jpg') 
    return render_template('game.html', title='Game', game_image=game_image, form=form, game_details=game_details)

@app.route('/add_new_game', methods=['POST', 'GET'])
def add():
    # message = "message"
    # if request.method == 'POST':
    #     try:
    #         name = request.form['new_game_name']
    #         release_year = request.form['release_year']
    #         age_rating = request.form['age_rating']
    #         score = request.form['score_rating']
    #         developer = request.form['developer']
    #         description = request.form['description']
    #         with sqlite3.connect("database.db") as connection:
    #             cursor = connection.cursor()
    #             cursor.execute("INSERT INTO Game (name, release_year, age_rating, score, developer, description) VALUES (?,?,?,?,?,?)", (name, release_year, age_rating, score, developer, description))
    #             connection.commit()
    #             message = "New Game Added Successfully"
    #     except:
    #         connection.rollback()
    #         message = "Insert Statement Failed, Rollback Complete"
    #     finally:
    #         connection.close()
    #         return render_template('add_new_game.html.', message = message)
    return render_template('add_new_game.html.')

@app.route('/view_games')
def view_all_games():
    # connection = sqlite3.connect("database.db")
    # connection.row_factory = sqlite3.Row
    # cursor = connection.cursor()
    # cursor.execute("SELECT * FROM Game")
    # rows = cursor.fetchall()
    return render_template('games_list.html')

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
