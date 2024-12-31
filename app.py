from flask import Flask, request, jsonify
import pyotp
from pqcrypto.sign.falcon_1024 import generate_keypair, sign, verify

app = Flask(__name__)

# Simulated database
users = {}
server_public_key, server_private_key = generate_keypair()

# Register user
@app.route('/register', methods=['POST'])
def register():
    user_id = request.json.get("user_id")
    if not user_id:
        return jsonify({"error": "User ID required"}), 400
    
    otp_secret = pyotp.random_base32()
    users[user_id] = {"otp_secret": otp_secret}
    return jsonify({"otp_secret": otp_secret, "public_key": server_public_key.hex()}), 200

# Authenticate user
@app.route('/authenticate', methods=['POST'])
def authenticate():
    user_id = request.json.get("user_id")
    otp = request.json.get("otp")
    if user_id not in users:
        return jsonify({"error": "User not registered"}), 404
    
    otp_secret = users[user_id]["otp_secret"]
    if not pyotp.TOTP(otp_secret).verify(otp):
        return jsonify({"error": "Invalid OTP"}), 401
    
    message = f"UserID:{user_id}, OTP:{otp}"
    signature = sign(message.encode(), server_private_key)
    return jsonify({"message": message, "signature": signature.hex()}), 200

# Verify authentication
@app.route('/verify', methods=['POST'])
def verify_auth():
    data = request.json
    message = data.get("message")
    signature = bytes.fromhex(data.get("signature"))
    
    if verify(message.encode(), signature, server_public_key):
        return jsonify({"status": "Authentication successful"}), 200
    return jsonify({"status": "Authentication failed"}), 401

if __name__ == '__main__':
    app.run(debug=True)
