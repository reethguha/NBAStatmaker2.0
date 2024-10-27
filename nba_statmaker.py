import requests

class NBAStatMaker:
    def __init__(self, auth_key):
        self.auth_key = auth_key
        self.base_url = "https://api.balldontlie.io/v1/players"
    
    # Function to search for player by name and return the player ID
    def get_player_id(self, search_term):
        url = f"{self.base_url}?search={search_term}"
        headers = {"Authorization": self.auth_key}  # Add the Authorization header with the key

        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            if data['data']:
                # Display a list of matching players and their details
                for idx, player in enumerate(data['data']):
                    print(f"{idx + 1}. {player['first_name']} {player['last_name']} - Team: {player['team']['full_name']}")
                
                # Let the user select the correct player if there are multiple results
                choice = int(input(f"Enter the number of the player you want (1-{len(data['data'])}): ")) - 1
                selected_player = data['data'][choice]
                return selected_player['id'], selected_player
            else:
                print("Player not found.")
                return None, None
        else:
            print(f"Failed to search for player. Status code: {response.status_code}")
            return None, None

    # Function to display player info
    def display_player_info(self, player_data):
        if player_data:
            print(f"Player Name: {player_data['first_name']} {player_data['last_name']}")
            print(f"Position: {player_data['position']}")
            
            # Get player attributes
            height = player_data.get('height', "N/A")
            weight = player_data.get('weight', "N/A")
            jersey_number = player_data.get('jersey_number', "N/A")
            college_attended = player_data.get('college', "N/A")
            draft_year = player_data.get('draft_year', "N/A")
            draft_round = player_data.get('draft_round', "N/A")
            draft_pick = player_data.get('draft_number', "N/A")

            print(f"Height: {height}")
            print(f"Weight: {weight} lbs")
            print(f"Team: {player_data['team']['full_name']}")
            print(f"Jersey Number: {jersey_number}")
            print(f"College: {college_attended}")
            print(f"Draft Info: Round {draft_round}, Pick {draft_pick}, in the {draft_year} Draft")

        else:
            print("No player data to display.")
    
    # Main method to handle player search and info display
    def run(self):
        search_term = input("Enter the player's name or part of their name: ").strip()
        player_id, player_data = self.get_player_id(search_term)
        
        if player_id:
            self.display_player_info(player_data)

# Example usage
if __name__ == "__main__":
    auth_key = "b2b9782d-fa82-470f-9092-411c9a66a986"  # Your API key here
    nba_stat_maker = NBAStatMaker(auth_key)
    nba_stat_maker.run()