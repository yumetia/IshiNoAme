// api.js
const API_URL = "https://ishinoame.onrender.com";

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
    console.log("Score received :", data);
  })
  .catch(error => {
    console.error("Erreur sending the score :", error);
  });
}


function fetchLeaderboard() {
  fetch(`${API_URL}/top`)
  .then(response => response.json())
  .then(data => {
    pyxelLeaderboardData = data;
    console.log("Leaderboard received :", data);
  })
  .catch(error => {
    console.error("Erreur getting leaderboard :", error);
  });
}

function getLeaderboard(){
  return pyxelLeaderboardData;
}


fetchLeaderboard();
pyxel.register("send_score", (score) => {
  const username = pyxel.globals.username || "Anonymous";
  sendScore(username, score);
});

