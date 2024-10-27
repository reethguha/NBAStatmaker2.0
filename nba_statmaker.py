from flask import Flask, request, jsonify
from flask_cors import CORS
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
import requests

class NBAStatMaker:
    def __init__(self, auth_key):
        self.auth_key = auth_key
        self.base_url = "https://api.balldontlie.io/v1/players"
    
    # Function to search for player by name and return the player ID
    def get_player_id(self, search_term):
        url = f"{self.base_url}?search={search_term}"
        headers = {"Authorization": self.auth_key}
        response = requests.get(url, headers=headers)
        return response.json()

    # Function to get detailed player info by player ID
    def get_player_info(self, player_id):
        url = f"{self.base_url}/{player_id}"
        headers = {"Authorization": self.auth_key}
        response = requests.get(url, headers=headers)
        return response.json()

    # Function to format and display player information
    def display_player_info(self, player_data):
        if player_data:
            info = {
                "Player Name": f"{player_data['first_name']} {player_data['last_name']}",
                "Position": player_data.get('position', 'N/A'),
                "Height": f"{player_data.get('height_feet', 'N/A')}-{player_data.get('height_inches', 'N/A')}",
                "Weight": player_data.get('weight_pounds', 'N/A'),
                "Team": player_data['team']['full_name'],
                "Jersey Number": player_data.get('jersey_number', 'N/A'),
                "College": player_data.get('college', 'N/A'),
                "Draft Year": player_data.get('draft', {}).get('year', 'N/A'),
                "Draft Round": player_data.get('draft', {}).get('round', 'N/A'),
                "Draft Pick": player_data.get('draft', {}).get('pick', 'N/A')
            }
            return info
        else:
            return {"error": "No player data to display."}

# Initialize NBAStatMaker with your API key
nba_stat_maker = NBAStatMaker(auth_key="b2b9782d-fa82-470f-9092-411c9a66a986")

# Flask route to search players
@app.route('/search_player', methods=['GET'])
def search_player():
    search_term = request.args.get('search')
    if not search_term:
        return jsonify({"error": "No search term provided"}), 400

    player_data = nba_stat_maker.get_player_id(search_term)
    return jsonify(player_data)

# Flask route to get detailed player info by player ID
@app.route('/get_player_info/<int:player_id>', methods=['GET'])
def get_player_info(player_id):
    player_data = nba_stat_maker.get_player_info(player_id)
    formatted_data = nba_stat_maker.display_player_info(player_data)
    return jsonify(formatted_data)

if __name__ == "__main__":
    app.run(debug=True)
