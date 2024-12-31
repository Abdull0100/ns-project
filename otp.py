import pyotp

# Generate a secret key for the user
def generate_otp_secret():
    return pyotp.random_base32()

# Generate an OTP for a user
def generate_otp(secret):
    totp = pyotp.TOTP(secret)
    return totp.now()

# Validate the OTP
def validate_otp(secret, otp):
    totp = pyotp.TOTP(secret)
    return totp.verify(otp)

# Example usage
user_secret = generate_otp_secret()
print("User Secret:", user_secret)

otp = generate_otp(user_secret)
print("Generated OTP:", otp)

# Simulate user entering the OTP
is_valid = validate_otp(user_secret, otp)
print("Is OTP valid?", is_valid)
