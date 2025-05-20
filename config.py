"""
Configuration settings for the multi-company user management system.
"""

# Company configurations
COMPANIES = {
    'A': {
        'name': 'Company A',
        'api_endpoint': 'http://company-a.example.com/api/users',
        'api_key': 'your_api_key_here',
        'db_config': {
            'host': 'localhost',
            'database': 'company_a_db',
            'user': 'db_user',
            'password': 'db_password'
        }
    },
    'B': {
        'name': 'Company B',
        'api_endpoint': 'http://company-b.example.com/api/users',
        'api_key': 'your_api_key_here',
        'db_config': {
            'host': 'localhost',
            'database': 'company_b_db',
            'user': 'db_user',
            'password': 'db_password'
        }
    },
    'C': {
        'name': 'Company C',
        'api_endpoint': 'http://company-c.example.com/api/users',
        'api_key': 'your_api_key_here',
        'db_config': {
            'host': 'localhost',
            'database': 'company_c_db',
            'user': 'db_user',
            'password': 'db_password'
        }
    }
}

# Current company identifier (change this based on where the code is deployed)
CURRENT_COMPANY = 'A'

# API settings
API_TIMEOUT = 30  # seconds
API_RETRY_ATTEMPTS = 3 