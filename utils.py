"""
Utility functions for database and API operations.
"""

import mysql.connector
import requests
from typing import List, Dict, Any
import logging
from config import COMPANIES, CURRENT_COMPANY, API_TIMEOUT, API_RETRY_ATTEMPTS

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_local_users() -> List[Dict[str, Any]]:
    """
    Retrieve users from the local database.
    
    Returns:
        List[Dict[str, Any]]: List of user dictionaries
    """
    try:
        db_config = COMPANIES[CURRENT_COMPANY]['db_config']
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return users
    except Exception as e:
        logger.error(f"Error fetching local users: {str(e)}")
        return []

def get_remote_users(company_id: str) -> List[Dict[str, Any]]:
    """
    Retrieve users from a remote company's API.
    
    Args:
        company_id (str): The ID of the company to fetch users from
        
    Returns:
        List[Dict[str, Any]]: List of user dictionaries
    """
    if company_id == CURRENT_COMPANY:
        return get_local_users()
    
    company_config = COMPANIES[company_id]
    headers = {
        'Authorization': f"Bearer {company_config['api_key']}",
        'Content-Type': 'application/json'
    }
    
    for attempt in range(API_RETRY_ATTEMPTS):
        try:
            response = requests.get(
                company_config['api_endpoint'],
                headers=headers,
                timeout=API_TIMEOUT
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching users from {company_id} (attempt {attempt + 1}): {str(e)}")
            if attempt == API_RETRY_ATTEMPTS - 1:
                return []

def get_all_users() -> Dict[str, List[Dict[str, Any]]]:
    """
    Retrieve users from all companies.
    
    Returns:
        Dict[str, List[Dict[str, Any]]]: Dictionary mapping company IDs to their user lists
    """
    all_users = {}
    
    for company_id in COMPANIES:
        if company_id == CURRENT_COMPANY:
            all_users[company_id] = get_local_users()
        else:
            all_users[company_id] = get_remote_users(company_id)
    
    return all_users 