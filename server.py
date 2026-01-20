import os
from flask import Flask, render_template, jsonify, send_from_directory
from flask_cors import CORS
from livekit import api
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, static_folder='public', static_url_path='')
CORS(app)

@app.route('/')
def index():
    # Serve the main HTML file
    return send_from_directory('public', 'index.html')

@app.route('/getToken')
def get_token():
    # 1. Retrieve API keys from environment variables
    api_key = os.getenv('LIVEKIT_API_KEY')
    api_secret = os.getenv('LIVEKIT_API_SECRET')

    if not api_key or not api_secret:
        return jsonify({'error': 'API Keys not found'}), 500

    # 2. Generate a random identity for the user
    participant_identity = f"user_{os.urandom(4).hex()}"
    room_name = "my-room"  # Must match the room name logic if dynamic

    # 3. Create access token with permissions to join, speak, and listen
    grant = api.VideoGrant(room_join=True, room=room_name)
    token = api.AccessToken(api_key, api_secret, identity=participant_identity)
    token.add_grant(grant)
    
    # Return the token and the LiveKit server URL to the client
    return jsonify({
        'token': token.to_jwt(),
        'url': os.getenv('LIVEKIT_URL')
    })

if __name__ == '__main__':
    print("Web Server running on http://localhost:5000")
    app.run(port=5000, debug=True)