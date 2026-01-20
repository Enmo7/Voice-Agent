import os
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from livekit import api
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, static_folder='public', static_url_path='')
CORS(app)

@app.route('/')
def index():
    return send_from_directory('public', 'index.html')

@app.route('/getToken')
def get_token():
   
    api_key = os.getenv('LIVEKIT_API_KEY')
    api_secret = os.getenv('LIVEKIT_API_SECRET')

    if not api_key or not api_secret:
        return jsonify({'error': 'API Keys not found'}), 500

 
    participant_identity = f"user_{os.urandom(4).hex()}"
    room_name = "my-room"

   
    grant = api.VideoGrants(room_join=True, room=room_name, can_publish=True, can_subscribe=True)
    
    
    token = api.AccessToken(api_key, api_secret) \
        .with_identity(participant_identity) \
        .with_grants(grant)
    
    return jsonify({
        'token': token.to_jwt(),
        'url': os.getenv('LIVEKIT_URL')
    })

if __name__ == '__main__':
    print("Web Server running on http://localhost:5000")
    app.run(port=5000, debug=True)