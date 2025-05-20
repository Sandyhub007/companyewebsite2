from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from whitenoise import WhiteNoise
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.wsgi_app = WhiteNoise(app.wsgi_app, root='static/')
app.secret_key = os.getenv('SECRET_KEY', os.urandom(24))

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///company_a.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Company configuration
COMPANY_NAME = "Company A"
COMPANY_B_URL = os.getenv('COMPANY_B_URL', 'http://company-b.example.com')
COMPANY_C_URL = os.getenv('COMPANY_C_URL', 'http://company-c.example.com')

# User model for database
class CompanyUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    department = db.Column(db.String(50), nullable=False)
    company = db.Column(db.String(50), nullable=False)

# Admin user model
class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id

# Initialize login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Mock admin database
users = {
    os.getenv('ADMIN_USERNAME', 'admin'): {
        'password': generate_password_hash(os.getenv('ADMIN_PASSWORD', 'admin123')),
        'role': 'admin'
    }
}

@login_manager.user_loader
def load_user(user_id):
    if user_id in users:
        return User(user_id)
    return None

# Initialize database with sample data
def init_db():
    with app.app_context():
        db.create_all()
        # Add sample users if database is empty
        if CompanyUser.query.count() == 0:
            sample_users = [
                CompanyUser(name='Mary Smith', email='mary.smith@company-a.com', department='Engineering', company='Company A'),
                CompanyUser(name='John Wang', email='john.wang@company-a.com', department='Marketing', company='Company A'),
                CompanyUser(name='Alex Bington', email='alex.bington@company-a.com', department='Sales', company='Company A'),
                CompanyUser(name='Sarah Johnson', email='sarah.johnson@company-a.com', department='HR', company='Company A'),
                CompanyUser(name='Michael Chen', email='michael.chen@company-a.com', department='Finance', company='Company A')
            ]
            db.session.add_all(sample_users)
            db.session.commit()

# Initialize database
init_db()

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
    
    # Get local users
    local_users = CompanyUser.query.filter_by(company=COMPANY_NAME).all()
    
    # Get users from other companies using CURL (requests)
    try:
        company_b_users = requests.get(f"{COMPANY_B_URL}/api/users").json()
    except:
        company_b_users = []
        flash('Could not fetch users from Company B', 'error')
    
    try:
        company_c_users = requests.get(f"{COMPANY_C_URL}/api/users").json()
    except:
        company_c_users = []
        flash('Could not fetch users from Company C', 'error')
    
    return render_template('admin_dashboard.html', 
                         local_users=local_users,
                         company_b_users=company_b_users,
                         company_c_users=company_c_users)

@app.route('/api/users')
def get_users():
    """API endpoint to get users from this company"""
    users = CompanyUser.query.filter_by(company=COMPANY_NAME).all()
    return jsonify([{
        'name': user.name,
        'email': user.email,
        'department': user.department,
        'company': user.company
    } for user in users])

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5001)), debug=True) 