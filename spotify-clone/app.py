from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'raaga_team3_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///raaga.db'
db = SQLAlchemy(app)

# Login System Setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# User Database Model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# 1. Create a list with 100 actually different songs
# Note: You need to find 100 different URLs/Images to make them truly unique.
DIFFERENT_SONGS = [
    {"title": "Kesariya", "artist": "Pritam", "img": "https://i.scdn.co/image/ab67616d0000b273c59bc8360667086055f1342a", "url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"},
    {"title": "Tum Hi Ho", "artist": "Arijit Singh", "img": "https://i.scdn.co/image/ab67616d0000b273760419ef8e94ca810052744e", "url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3"},
    {"title": "Pasoori", "artist": "Ali Sethi", "img": "https://i.scdn.co/image/ab67616d0000b27374092b37c046e7f804708767", "url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3"},
    # ... Add 97 more unique dictionaries here ...
]

# 2. Change your SONGS variable to just use that list
# Remove the old 'for i in range(1000)' line!
SONGS = DIFFERENT_SONGS

# --- ROUTES ---

@app.route('/')
@login_required
def home():
    return render_template('index.html', songs=SONGS, user=current_user.username)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and user.password == request.form['password']:
            login_user(user)
            return redirect(url_for('home'))
    return render_template('auth.html', type='Login')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Simple save (In a real app, use password hashing!)
        new_user = User(username=request.form['username'], password=request.form['password'])
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('auth.html', type='Signup')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all() # Builds the database file raaga.db
    app.run(debug=True)