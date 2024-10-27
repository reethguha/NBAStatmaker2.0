const API_KEY = "b2b9782d-fa82-470f-9092-411c9a66a986"; // Your API key

document.getElementById("player-form").addEventListener("submit", function(event) {
    event.preventDefault(); // Prevent the form from submitting traditionally

    let playerName = document.getElementById("playername").value;
    if (playerName === "") {
        alert("Please enter a player's name");
        return;
    }

    // Clear previous search results
    document.getElementById("players-table").innerHTML = `
        <tr>
            <th>Player Name</th>
            <th>Position</th>
            <th>Select</th>
        </tr>
    `;

    // Fetch matching players from Flask backend
    fetch(`http://127.0.0.1:5000/search_player?search=${playerName}`)
    .then(response => response.json())
    .then(data => {
        if (data.data && data.data.length > 0) {
            data.data.forEach((player, index) => {
                // Create a row for each matching player
                let playerRow = `
                    <tr>
                        <td>${player.first_name} ${player.last_name}</td>
                        <td>${player.position ? player.position : 'N/A'}</td>
                        <td><button onclick="getPlayerInfo(${player.id})">Select</button></td>
                    </tr>
                `;
                document.getElementById("players-table").innerHTML += playerRow;
            });
        } else {
            alert("No matching players found");
        }
    })
    .catch(error => {
        console.error("Error fetching player data:", error);
        alert("An error occurred while fetching player data.");
    });
});

// Fetch detailed player info and display in player info table
function getPlayerInfo(playerId) {
    fetch(`http://127.0.0.1:5000/get_player_info/${playerId}`)
    .then(response => response.json())
    .then(player => {
        // Clear the player info table and insert new details
        document.getElementById("player-info-table").innerHTML = `
            <tr>
                <th>Player Name</th>
                <th>Position</th>
                <th>Height</th>
                <th>Weight</th>
                <th>Team</th>
                <th>Jersey Number</th>
                <th>College</th>
                <th>Draft Year</th>
                <th>Draft Round</th>
                <th>Draft Pick</th>
            </tr>
            <tr>
                <td>${player["Player Name"]}</td>
                <td>${player["Position"]}</td>
                <td>${player["Height"]}</td>
                <td>${player["Weight"]} lbs</td>
                <td>${player["Team"]}</td>
                <td>${player["Jersey Number"]}</td>
                <td>${player["College"]}</td>
                <td>${player["Draft Year"]}</td>
                <td>${player["Draft Round"]}</td>
                <td>${player["Draft Pick"]}</td>
            </tr>
        `;
    })
    .catch(error => {
        console.error("Error fetching detailed player info:", error);
        alert("An error occurred while fetching detailed player info.");
    });
}
