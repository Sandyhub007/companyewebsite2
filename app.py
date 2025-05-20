from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from whitenoise import WhiteNoise
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.wsgi_app = WhiteNoise(app.wsgi_app, root='static/')
app.secret_key = os.getenv('SECRET_KEY', os.urandom(24))
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Mock user database
users = {
    os.getenv('ADMIN_USERNAME', 'admin'): {
        'password': generate_password_hash(os.getenv('ADMIN_PASSWORD', 'admin123')),
        'role': 'admin'
    }
}

# Mock website users list
website_users = [
    {'name': 'Mary Smith', 'email': 'mary.smith@company.com', 'department': 'Engineering'},
    {'name': 'John Wang', 'email': 'john.wang@company.com', 'department': 'Marketing'},
    {'name': 'Alex Bington', 'email': 'alex.bington@company.com', 'department': 'Sales'},
    {'name': 'Sarah Johnson', 'email': 'sarah.johnson@company.com', 'department': 'HR'},
    {'name': 'Michael Chen', 'email': 'michael.chen@company.com', 'department': 'Finance'}
]

class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id

@login_manager.user_loader
def load_user(user_id):
    if user_id in users:
        return User(user_id)
    return None

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username in users and check_password_hash(users[username]['password'], password):
            user = User(username)
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if current_user.id != os.getenv('ADMIN_USERNAME', 'admin'):
        flash('Access denied', 'error')
        return redirect(url_for('home'))
    return render_template('admin_dashboard.html', users=website_users)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5001)), debug=True) 