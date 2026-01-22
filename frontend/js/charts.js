function fitCanvasToContainer(canvas) {
  const parent = canvas.parentElement;
  if (!parent) return;

  const cssWidth = parent.clientWidth;
  const cssHeight = canvas.height; // mantemos altura fixa

  // Ajusta para o tamanho do container (retina-safe)
  const dpr = window.devicePixelRatio || 1;
  canvas.style.width = cssWidth + "px";
  canvas.style.height = cssHeight + "px";
  canvas.width = Math.floor(cssWidth * dpr);
  canvas.height = Math.floor(cssHeight * dpr);

  const ctx = canvas.getContext("2d");
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0); // desenhar em "CSS pixels"
}

function renderTopRiskChart(canvasId, users, maxBars = 6) {
  const canvas = document.getElementById(canvasId);
  if (!canvas) return;

  fitCanvasToContainer(canvas);

  const ctx = canvas.getContext("2d");
  const width = canvas.clientWidth;
  const height = canvas.clientHeight;

  ctx.clearRect(0, 0, width, height);

  const items = (users || [])
    .slice()
    .sort((a, b) => b.score - a.score)
    .slice(0, maxBars);

  if (items.length === 0) {
    ctx.fillStyle = "#9da7b3";
    ctx.font = "14px Segoe UI";
    ctx.fillText("No data yet. Add events to see risk analytics.", 12, 28);
    return;
  }

  // Layout
  const padding = 16;
  const titleH = 26;
  const leftLabelW = 160;
  const rightScoreW = 48;
  const chartTop = padding + titleH;
  const chartBottom = height - padding;
  const chartH = chartBottom - chartTop;

  const gap = 10;
  const barH = Math.max(18, Math.floor((chartH - gap * (items.length - 1)) / items.length));

  const maxScore = Math.max(...items.map((x) => x.score), 1);

  // Title
  ctx.fillStyle = "#e6edf3";
  ctx.font = "14px Segoe UI";
  ctx.fillText("Top Risk Users", padding, padding + 14);

  const barX = padding + leftLabelW;
  const barMaxW = Math.max(120, width - padding - barX - rightScoreW);

  items.forEach((u, i) => {
    const y = chartTop + i * (barH + gap);
    const score = u.score;

    // Label
    ctx.fillStyle = "#9da7b3";
    ctx.font = "12px Segoe UI";
    ctx.fillText(u.user_id, padding, y + barH - 5);

    // Background bar
    ctx.fillStyle = "rgba(255,255,255,0.06)";
    ctx.fillRect(barX, y, barMaxW, barH);

    // Fill
    const fillW = Math.max(6, Math.floor((score / maxScore) * barMaxW));
    ctx.fillStyle = "rgba(47,129,247,0.85)";
    ctx.fillRect(barX, y, fillW, barH);

    // Score
    ctx.fillStyle = "#e6edf3";
    ctx.font = "12px Segoe UI";
    ctx.fillText(String(score), barX + barMaxW + 12, y + barH - 5);
  });
}

// Re-render on resize so it never overflows
window.addEventListener("resize", () => {
  if (window.__lastUsersForChart) {
    renderTopRiskChart("top-risk-chart", window.__lastUsersForChart);
  }
});

window.Charts = {
  renderTopRiskChart: (id, users) => {
    window.__lastUsersForChart = users || [];
    renderTopRiskChart(id, users || []);
  },
};
