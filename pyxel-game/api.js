// api.js
const API_URL = "url...";

let pyxelLeaderboardData = [];


function sendScore(username, score) {
  fetch(`${API_URL}/submit-score`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ username, score })
  })
  .then(response => response.json())
  .then(data => {
    console.log("Score envoyé :", data);
  })
  .catch(error => {
    console.error("Erreur lors de l'envoi du score :", error);
  });
}


function fetchLeaderboard() {
  fetch(`${API_URL}/top`)
    .then(response => response.json())
    .then(data => {
      pyxelLeaderboardData = data;
      console.log("Leaderboard récupéré :", data);
    })
    .catch(error => {
      console.error("Erreur lors de la récupération du leaderboard :", error);
    });
}

fetchLeaderboard();
