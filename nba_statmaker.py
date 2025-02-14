from flask import Flask, jsonify, request 
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  

class NBAStatMaker:
    def __init__(self, auth_key):
        self.auth_key = auth_key
        self.base_url = "https://api.balldontlie.io/v1/players"

    """
    Once the user enters a player's name, we return all the players in the api that match or have partial 
    names to the one entered by the user.
    """
    def get_player_id(self, search_term):
        url = f"{self.base_url}?search={search_term}"
        headers = {"Authorization": self.auth_key}  
        response = requests.get(url, headers=headers)  

        if response.status_code == 200:
            data = response.json()
            return data['data']  
        else:
            return None 

    """
    After the specific player is selected, return the information of the player.
    """
    def get_player_info(self, player_id):
        url = f"{self.base_url}/{player_id}"
        headers = {"Authorization": self.auth_key} 
        response = requests.get(url, headers=headers)  

        if response.status_code == 200:
            data = response.json()
            return data['data']  
        else:
            return None  # Handle failure

# Initialize NBAStatMaker
nba_stat_maker = NBAStatMaker(auth_key="b2b9782d-fa82-470f-9092-411c9a66a986")

"""
Flask route to search for the player 
"""
@app.route('/search_player', methods=['GET'])
def search_player():
    search_term = request.args.get('search')
    players = nba_stat_maker.get_player_id(search_term)
    if players:
        return jsonify({'data': players}), 200
    else:
        return jsonify({"error": "No players found"}), 404

"""
Flask route to return the player's information
"""
@app.route('/get_player_info/<int:player_id>', methods=['GET'])
def get_player_info(player_id):
    player_info = nba_stat_maker.get_player_info(player_id)
    if player_info:
        return jsonify(player_info), 200
    else:
        return jsonify({"error": "Player not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)