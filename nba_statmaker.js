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
            data.data.forEach((player) => {
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
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
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
                <td>${player.first_name} ${player.last_name}</td>
                <td>${player.position ? player.position : 'N/A'}</td>
                <td>${player.height ? player.height : 'N/A'}</td>
                <td>${player.weight ? player.weight + ' lbs' : 'N/A'}</td>
                <td>${player.team ? player.team.full_name : 'N/A'}</td>
                <td>${player.jersey_number ? player.jersey_number : 'N/A'}</td>
                <td>${player.college ? player.college : 'N/A'}</td>
                <td>${player.draft_year ? player.draft_year : 'N/A'}</td>
                <td>${player.draft_round ? player.draft_round : 'N/A'}</td>
                <td>${player.draft_number ? player.draft_number : 'N/A'}</td>
            </tr>
        `;
    })
    .catch(error => {
        console.error("Error fetching detailed player info:", error);
        alert("An error occurred while fetching detailed player info.");
    });
}
