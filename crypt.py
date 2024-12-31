from pqcrypto.sign.falcon_1024 import generate_keypair, sign, verify

# Generate key pair
server_public_key, server_private_key = generate_keypair()

# Create a signed message
def sign_auth_message(user_id, otp, private_key):
    message = f"UserID:{user_id}, OTP:{otp}"
    signature = sign(message.encode(), private_key)
    return message, signature

# Verify the signed message
def verify_auth_message(message, signature, public_key):
    return verify(message.encode(), signature, public_key)
