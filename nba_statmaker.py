from flask import Flask, jsonify, request  # Ensure request is imported
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

class NBAStatMaker:
    def __init__(self, auth_key):
        self.auth_key = auth_key
        self.base_url = "https://api.balldontlie.io/v1/players"

    def get_player_id(self, search_term):
        url = f"{self.base_url}?search={search_term}"
        headers = {"Authorization": self.auth_key}  # Add Authorization header
        response = requests.get(url, headers=headers)  # Include headers in request

        if response.status_code == 200:
            data = response.json()
            return data['data']  # Return all matching players
        else:
            return None  # Handle failure

    def get_player_info(self, player_id):
        url = f"{self.base_url}/{player_id}"
        headers = {"Authorization": self.auth_key}  # Add Authorization header
        response = requests.get(url, headers=headers)  # Include headers in request

        if response.status_code == 200:
            data = response.json()
            return data['data']  # Return the player data
        else:
            return None  # Handle failure

# Initialize NBAStatMaker
nba_stat_maker = NBAStatMaker(auth_key="b2b9782d-fa82-470f-9092-411c9a66a986")

@app.route('/search_player', methods=['GET'])
def search_player():
    search_term = request.args.get('search')  # Use request.args
    players = nba_stat_maker.get_player_id(search_term)
    if players:
        return jsonify({'data': players}), 200
    else:
        return jsonify({"error": "No players found"}), 404

@app.route('/get_player_info/<int:player_id>', methods=['GET'])
def get_player_info(player_id):
    player_info = nba_stat_maker.get_player_info(player_id)
    if player_info:
        return jsonify(player_info), 200
    else:
        return jsonify({"error": "Player not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
