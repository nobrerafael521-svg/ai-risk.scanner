function scoreClass(score) {
  if (score >= 50) return "score-high";
  if (score >= 20) return "score-medium";
  return "score-low";
}

function reasonsToText(reasonsObj) {
  if (!reasonsObj) return "-";
  const entries = Object.entries(reasonsObj);
  if (entries.length === 0) return "-";

  return entries
    .sort((a, b) => b[1] - a[1])
    .map(([reason, count]) => `${reason} (x${count})`)
    .join(", ");
}

async function loadDashboard() {
  try {
    // KPIs
    const summary = await window.API.get("/risk/summary");
    document.getElementById("kpi-total-events").textContent = summary.total_events ?? "0";
    document.getElementById("kpi-total-users").textContent = summary.total_users ?? "0";
    document.getElementById("kpi-high-risk").textContent = summary.high_risk_users ?? "0";

    // Users risk
    const users = await window.API.get("/risk/users");
    const items = users.items || [];

    // Chart (Top risk users)
    if (window.Charts) {
      window.Charts.renderTopRiskChart("top-risk-chart", items);
    }

    // Table
    const tbody = document.querySelector("#risk-table tbody");
    tbody.innerHTML = "";

    items.forEach((u) => {
      const tr = document.createElement("tr");

      const tdUser = document.createElement("td");
      tdUser.textContent = u.user_id;

      const tdScore = document.createElement("td");
      tdScore.textContent = u.score;
      tdScore.className = scoreClass(u.score);

      const tdHighEvents = document.createElement("td");
      tdHighEvents.textContent = u.high_risk_events;

      const tdReasons = document.createElement("td");
      tdReasons.textContent = reasonsToText(u.reasons);

      tr.appendChild(tdUser);
      tr.appendChild(tdScore);
      tr.appendChild(tdHighEvents);
      tr.appendChild(tdReasons);

      tbody.appendChild(tr);
    });
  } catch (err) {
    console.error(err);
    alert(
      "Failed to load dashboard.\n\n" +
        "Make sure the backend is running at http://127.0.0.1:8000\n\n" +
        "Error: " + err.message
    );
  }
}

document.addEventListener("DOMContentLoaded", loadDashboard);

