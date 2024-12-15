from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import pickle
import numpy as np


app = Flask(__name__)
app.secret_key = 'testkey1234'

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

MODEL_PATH = r"D:\\Semester VII\\MLOps\\Class-Activity-7\\models\\model.pkl"
with open(MODEL_PATH, "rb") as model_file:
    model = pickle.load(model_file)

@app.route('/')
def home():
    if 'user' in session:
        return redirect(url_for('main'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user' in session:
        return redirect(url_for('main'))

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            session['user'] = email
            return redirect(url_for('main'))
        else:
            print('Invalid email or password', 'error')

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if 'user' in session:
        return redirect(url_for('main'))

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if User.query.filter_by(email=email).first():
            print('User already exists', 'error')
            return redirect(url_for('login'))
        else:
            new_user = User(email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            session['user'] = email
            print('User registered successfully', 'success')
            return redirect(url_for('main'))
            

    return render_template('signup.html')

@app.route('/main')
def main():
    if 'user' not in session:
        return redirect(url_for('login'))

    return render_template('main.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'user' not in session:
        return redirect(url_for('login'))

    try:
        # Get input values
        humid = float(request.form['humid'])
        wind_sp = float(request.form['wind_sp'])
        cloud_cover = float(request.form['cloud_cover'])
        precipitation = float(request.form['precipitation'])

        # Prepare the input features
        input_features = np.array([[humid, wind_sp, cloud_cover, precipitation]])

        # Make prediction
        prediction = model.predict(input_features)[0][0]

        return render_template('main.html', prediction=prediction)
    except Exception as e:
        print(f"Error during prediction: {e}")
        return render_template('main.html', prediction="Error during prediction. Please try again.")


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    # Create the database tables on the first run
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=9876, debug=True)
