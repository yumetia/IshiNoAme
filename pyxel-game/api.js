const API_URL = "https://ishinoame.onrender.com";
let pyxelLeaderboardData = [];

function sendScore(username, score) {
  fetch(`${API_URL}/submit-score`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, score })
  }).then(r => r.json())
    .then(data => console.log("Score envoyé:", data))
    .catch(e => console.error("Erreur POST:", e));
}

async function fetchLeaderboard() {
  return fetch(`${API_URL}/top`)
    .then(r => r.json())
    .then(data => {
      pyxelLeaderboardData = data;
      console.log("Leaderboard reçu:", data);
    })
    .catch(e => console.error("Erreur GET:", e));
}

fetchLeaderboard().then(() => {
  pyxel.register("get_leaderboard", () => {
    console.log("JS renvoie leaderboard:", pyxelLeaderboardData);
    return pyxelLeaderboardData;
  });

  pyxel.register("sendScore", (username, score) => {
    console.log("JS reçoit score:", username, score);
    sendScore(username, score);
  });
});
