import os
import json
import uuid
import bcrypt
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this in production

# File paths
USERS_FILE = 'users.json'

# Initialize users file if it doesn't exist
if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, 'w') as f:
        json.dump({}, f)

def load_users():
    with open(USERS_FILE, 'r') as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=4)

@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password').encode('utf-8')
        
        users = load_users()
        user = users.get(username)
        
        if user and bcrypt.checkpw(password, user['password'].encode('utf-8')):
            session['username'] = username
            return jsonify({'success': True, 'redirect': url_for('dashboard')})
        else:
            return jsonify({'success': False, 'message': 'Invalid username or password'})
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password').encode('utf-8')
        confirm_password = request.form.get('confirm_password').encode('utf-8')
        address = request.form.get('address')
        
        # Validation
        if not all([username, password, confirm_password, address]):
            return jsonify({'success': False, 'message': 'All fields are required'})
        
        if password != confirm_password:
            return jsonify({'success': False, 'message': 'Passwords do not match'})
        
        users = load_users()
        if username in users:
            return jsonify({'success': False, 'message': 'Username already exists'})
        
        # Hash password
        hashed = bcrypt.hashpw(password, bcrypt.gensalt()).decode('utf-8')
        
        # Create user
        users[username] = {
            'id': str(uuid.uuid4()),
            'password': hashed,
            'address': address
        }
        
        save_users(users)
        return jsonify({'success': True, 'redirect': url_for('login')})
    
    return render_template('signup.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    users = load_users()
    user = users.get(session['username'])
    return render_template('dashboard.html', username=session['username'], address=user['address'])

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)