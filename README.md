# Company Website with Secure Admin Section

This is a Flask-based company website with a secure admin section that requires authentication to access user information.

## Local Development Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a .env file with the following variables:
```
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123
```

4. Run the application:
```bash
python app.py
```

5. Access the website at `http://localhost:5000`

## Deployment

### Option 1: Deploy to Heroku

1. Install the Heroku CLI and login:
```bash
heroku login
```

2. Create a new Heroku app:
```bash
heroku create your-app-name
```

3. Set environment variables:
```bash
heroku config:set SECRET_KEY=your-secret-key-here
heroku config:set ADMIN_USERNAME=admin
heroku config:set ADMIN_PASSWORD=your-secure-password
```

4. Deploy the application:
```bash
git push heroku main
```

### Option 2: Deploy to a VPS (e.g., DigitalOcean, AWS EC2)

1. Set up your server with Python 3.8+ and nginx

2. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```

3. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Create .env file with production settings

6. Set up Gunicorn as a service:
```bash
sudo nano /etc/systemd/system/company-website.service
```

Add the following configuration:
```ini
[Unit]
Description=Company Website Gunicorn Service
After=network.target

[Service]
User=your-user
Group=your-group
WorkingDirectory=/path/to/your/app
Environment="PATH=/path/to/your/app/venv/bin"
ExecStart=/path/to/your/app/venv/bin/gunicorn --workers 3 --bind unix:company-website.sock -m 007 app:app

[Install]
WantedBy=multi-user.target
```

7. Start and enable the service:
```bash
sudo systemctl start company-website
sudo systemctl enable company-website
```

8. Configure nginx as a reverse proxy:
```bash
sudo nano /etc/nginx/sites-available/company-website
```

Add the following configuration:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        include proxy_params;
        proxy_pass http://unix:/path/to/your/app/company-website.sock;
    }
}
```

9. Enable the site and restart nginx:
```bash
sudo ln -s /etc/nginx/sites-available/company-website /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

## Security Considerations

1. Always use HTTPS in production
2. Keep your dependencies updated
3. Use strong passwords
4. Regularly rotate your SECRET_KEY
5. Monitor your application logs
6. Implement rate limiting for login attempts
7. Use secure headers (HSTS, CSP, etc.)

## Features
- Public company information
- Secure admin section
- User management system
- Responsive design 