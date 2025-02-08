"""
Authentication Service Module

This module handles all authentication-related functionality including password hashing,
verification, and JWT token generation.

Dependencies:
    - bcrypt: For password hashing
    - PyJWT: For JWT token handling
    - python-dotenv: For environment variable management

Environment Variables Required:
    - SECRET_KEY: Secret key for JWT token signing
"""

import bcrypt
import jwt
import datetime
import os
from dotenv import load_dotenv 
from datetime import datetime, timedelta

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
print(SECRET_KEY)
ALGORITHM = "HS256"

def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt.

    Args:
        password (str): Plain text password to hash

    Returns:
        str: Hashed password as UTF-8 string

    Example:
        >>> hashed = hash_password("mypassword123")
    """
    # Convert the password to bytes
    password_bytes = password.encode('utf-8')
    # Generate salt and hash the password
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    # Return the hash as a string
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash.

    Args:
        plain_password (str): Plain text password to verify
        hashed_password (str): Hashed password to compare against

    Returns:
        bool: True if password matches, False otherwise

    Example:
        >>> is_valid = verify_password("mypassword123", hashed_password)
    """
    # Convert passwords to bytes for comparison
    password_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    # Verify the password
    return bcrypt.checkpw(password_bytes, hashed_bytes)

def create_access_token(email: str):
    """
    Create a JWT access token for a user.

    Args:
        email (str): User's email address

    Returns:
        str: JWT token encoded as a string

    Note:
        Token expires in 24 hours from creation

    Example:
        >>> token = create_access_token("user@example.com")
    """
    expire = datetime.utcnow() + timedelta(days=1)
    payload = {"sub": email, "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
