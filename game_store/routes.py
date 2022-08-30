from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from game_store import app, db, bcrypt
from game_store.forms import RegistrationForm, LoginForm, UpdateGameForm, AddGameForm, SearchForm
from game_store.models import User, Game

@app.route('/')
@app.route('/home')
@app.route('/view_games')
def view_all_games():
    all_games = Game.query.all()
    return render_template('games_list.html', all_games=all_games)

# Register a New Account
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

# Login Function
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('view_all_games'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('view_all_games'))
        else:
            flash("Login Unsucessful. Please check email and password", 'danger')
    return render_template('login.html', title='Login', form=form)

# Logout Function
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('view_all_games'))

# Create New Records in the Game Table on the Database
@app.route('/add_new_game', methods=['GET', 'POST'])
@login_required
def add_new_game():
    form = AddGameForm()
    if form.validate_on_submit():
        new_game = Game(name=form.name.data,
        release_year=form.release_year.data,
        age_rating=form.age_rating.data,
        score=form.score.data,
        developer=form.developer.data,
        description=form.description.data)
        db.session.add(new_game)
        db.session.commit()
        flash("New Game Added Successfully", "success")
        return redirect(url_for('view_all_games'))
    return render_template('add_new_game.html', title='Add New Game', form=form)

@app.route('/game/<int:game_id>')
@login_required
def game(game_id):
    game_instance = Game.query.get_or_404(game_id)
    return render_template('game.html', title=game_instance.name, game_instance=game_instance)

@app.route('/game/<int:game_id>/update', methods=['GET', 'POST'])
@login_required
def update_game(game_id):
    game_instance = Game.query.get_or_404(game_id)
    form=UpdateGameForm()
    if form.validate_on_submit():
        game_instance.name = form.name.data
        game_instance.release_year = form.release_year.data
        game_instance.age_rating = form.age_rating.data
        game_instance.score = form.score.data
        game_instance.developer = form.developer.data
        game_instance.description = form.description.data
        db.session.commit()
        flash(f"{game_instance.name} Has Been Updated", 'success')
        return redirect(url_for('view_all_games'))

    elif request.method == 'GET':
        form.name.data = game_instance.name
        form.release_year.data = game_instance.release_year
        form.age_rating.data = game_instance.age_rating
        form.score.data = game_instance.score
        form.developer.data = game_instance.developer
        form.description.data = game_instance.description
    return render_template('add_new_game.html', title=f"Update { game_instance.name }", form=form)



# # Update Records in the Game Table on the Database
# @app.route('/game/<id:game_id>', methods=['GET', 'POST'])
# @login_required
# def update_game(game_id):
#     game_instance = Game.query.get(game_id)
#     form = UpdateGameForm()
#     if form.validate_on_submit():
#         game_instance.name = form.name.data
#         game_instance.release_year = form.release_year.data
#         game_instance.age_rating = form.age_rating.data
#         game_instance.score = form.score.data
#         game_instance.developer = form.developer
#         game_instance.description = form.description
#         db.session.commit()
#         flash(f"{game_instance.name} Has Been Updated", 'success')
#         return redirect(url_for('view_all_games'))

#     # elif request.method == 'GET':
#     #     form.name.data = form.name
#     #     form.release_year.data = form.release_year
#     #     form.age_rating.data = form.age_rating
#     #     form.score.data = form.score
#     #     form.developer.data = form.developer
#     #     form.description.data = form.description

#     return render_template('game.html', form=form, game_instance=game_id)


@app.route('/game/<int:game_id>/delete', methods=['POST'])
@login_required
def delete_game(game_id):
    game_instance = Game.query.get(game_id)
    db.session.delete(game_instance)
    db.session.commit()
    flash('Game deleted', 'success')
    return redirect(url_for('view_all_games'))


# Search Bar Functionality
@app.context_processor
def search_data():
    form = SearchForm()
    return dict(form=form)

@app.route('/search', methods=['POST'])
def search():
    form = SearchForm()
    games = Game.query
    if form.validate_on_submit():
        searched_game = form.searched.data
        games = games.filter(Game.name.like('%' + searched_game + '%'))
        games = games.order_by(Game.name).all()
        return render_template('search.html', form=form, searched=searched_game, games=games)
    else:
        return render_template('search_error.html')