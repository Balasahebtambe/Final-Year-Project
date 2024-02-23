from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import bcrypt

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Change this to a secure key
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '#Bala.123'
app.config['MYSQL_DB'] = 'college'

mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        Name = request.form['Name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO users (name, email, password, confirm_password) VALUES (%s, %s, %s, %s)",
                      (Name, email, hashed_password))
        mysql.connection.commit()
        cursor.close()

        session['email'] = email  # Log in the user after sign-up
        return redirect(url_for('dashboard'))

    return render_template('Sign-Up.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password_candidate = request.form['password']

        cursor = mysql.connection.cursor()
        result = cursor.execute("SELECT * FROM users WHERE email = %s", (email,))

        if result > 0:
            data = cursor.fetchone()
            password = data['password']

            if bcrypt.checkpw(password_candidate.encode('utf-8'), password.encode('utf-8')):
                session['email'] = email
                return redirect(url_for('dashboard'))
            else:
                return render_template('Sign-In.html', error='Invalid password')
        else:
            return render_template('Sign-In.html', error='Email not found')

    return render_template('Sign-In.html')

@app.route('/dashboard')
def dashboard():
    if 'email' in session:
        return f"Logged in as {session['email']}. Welcome to the dashboard!"
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
