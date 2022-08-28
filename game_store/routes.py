from flask import render_template, url_for, request, g, flash, redirect
from flask_login import login_user, current_user, logout_user, login_required
from game_store import app, db, bcrypt
from game_store.forms import RegistrationForm, LoginForm, UpdateGameForm, AddGameForm
from game_store.models import User, Game

@app.route('/')
@app.route('/home')
@app.route('/view_games')
def view_all_games():
    all_games = Game.query.all()
    return render_template('games_list.html', all_games=all_games)

@app.route('/new_game_added')
def game_added():
    return render_template('new_game_added.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('view_all_games'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("Account Created Successfully", 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('view_all_games'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('view_all_games'))
        else:
            flash("Login Unsucessful. Please check email and password", 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('view_all_games'))

@app.route('/game')
@login_required
def game():
    form = UpdateGameForm()
    game_details = Game.query.first()
    # Later fix the images for each specific game within the databse Game(game.game_iamge) table
    # game_image = url_for('static', filename='game_images/' + 'default.jpg') 
    return render_template('game.html', title='Game', form=form, game_details=game_details)

@app.route('/add_new_game', methods=['POST', 'GET'])
@login_required
def add():
    form = AddGameForm()
    if form.validate_on_submit():
        new_game = Game(name=form.name.data, release_year=form.release_year.data, age_rating=form.age_rating.data, score=form.score.data, developer=form.developer.data, description=form.description.data)
        db.session.add(new_game)
        db.session.commit()
        flash("New Game Added Successfully", "success")
        return redirect(url_for('view_all_games'))
    return render_template('add_new_game.html', title = 'Add New Game', form=form)

# @app.route('/test_view_games')
# def test_view_games():
#     connection = sqlite3.connect("database.db")
#     connection.row_factory = sqlite3.Row
#     cur = connection.cursor()
#     cur.execute("SELECT * FROM Game")
#     rows = cur.fetchall()
#     return render_template("test_view_games.html", rows = rows)