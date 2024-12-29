import hashlib
import os

# Generate a password hash
def hash_password(password: str, salt: bytes = None):
    salt = salt or os.urandom(16)  # Generate a new salt if not provided
    password_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    print(password_hash)
    return salt, password_hash

# Verify a password
def verify_password(password: str, salt: bytes, stored_hash: bytes):
    _, new_hash = hash_password(password, salt)
    return new_hash == stored_hash

# Example usage
password = "securepassword123"
salt, stored_hash = hash_password(password)
print(verify_password("securepassword123", salt, stored_hash))  # Output: True
