from game_store import db, login_manager
from flask_login import UserMixin

# Flask library for storing User sessions on the web page when logging in
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    
    def __repr__(self):
        return f"User('{self.username}', {self.email})"

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True, nullable=False)
    release_year = db.Column(db.Integer, nullable=False)
    age_rating = db.Column(db.Integer, nullable=False)
    score = db.Column(db.Float, nullable=False)
    developer = db.Column(db.String(60), nullable=False)
    description = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"Game('{self.name}', {self.release_year}, {self.age_rating}, {self.score}, {self.developer}, {self.description})"
