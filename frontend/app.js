const API_BASE = `${window.location.protocol}//${window.location.hostname}:8000`;
let currentSessionId = null;

const sessionForm = document.getElementById('session-form');
const brewForm = document.getElementById('brew-form');
const recommendBtn = document.getElementById('recommend-btn');
const recommendationOutput = document.getElementById('recommendation-output');
const sessionIdInput = document.getElementById('session-id');
const sessionListOutput = document.getElementById('session-list-output');
const brewListOutput = document.getElementById('brew-list-output');

function renderSessions(sessions) {
  if (!sessions.length) {
    sessionListOutput.innerHTML = '<div class="muted">No sessions yet.</div>';
    return;
  }

  const items = sessions.map((session) => {
    const activeClass = session.id === currentSessionId ? 'active' : '';
    return `
      <div class="session-item ${activeClass}" data-session-id="${session.id}">
        <strong>#${session.id}</strong> · ${session.goal_type || 'Session'}<br />
        <span class="muted">Coffee bean ${session.coffee_bean_id} · ${session.status}</span>
      </div>
    `;
  }).join('');

  sessionListOutput.innerHTML = `<div class="session-list">${items}</div>`;

  sessionListOutput.querySelectorAll('.session-item').forEach((item) => {
    item.addEventListener('click', () => {
      currentSessionId = Number(item.dataset.sessionId);
      sessionIdInput.value = currentSessionId;
      refreshBrewList();
      renderSessions(sessions);
    });
  });
}

async function refreshSessionList() {
  try {
    const response = await fetch(`${API_BASE}/dial-in-sessions/`);
    const sessions = await response.json();
    renderSessions(sessions);
  } catch (error) {
    sessionListOutput.innerHTML = `<div class="muted">Failed to load sessions: ${error.message}</div>`;
  }
}

function renderBrews(brews) {
  if (!brews.length) {
    brewListOutput.innerHTML = '<div class="muted">No brews logged yet for this session.</div>';
    return;
  }

  const cards = brews.map((brew) => {
    return `
      <div class="brew-card">
        <strong>Brew #${brew.id}</strong><br />
        <span class="muted">Score: ${brew.overall_score} · Ratio: ${brew.ratio}</span><br />
        <span class="muted">Grind: ${brew.grind_setting} · Temp: ${brew.water_temperature}°C</span><br />
        <div>${brew.notes || 'No notes added.'}</div>
      </div>
    `;
  }).join('');

  brewListOutput.innerHTML = cards;
}

async function refreshBrewList() {
  if (!currentSessionId) {
    brewListOutput.innerHTML = '<div class="muted">No session selected.</div>';
    return;
  }

  try {
    const response = await fetch(`${API_BASE}/dial-in-sessions/${currentSessionId}/details`);
    const details = await response.json();
    renderBrews(details.brews || []);
  } catch (error) {
    brewListOutput.innerHTML = `<div class="muted">Failed to load brews: ${error.message}</div>`;
  }
}

sessionForm.addEventListener('submit', async (event) => {
  event.preventDefault();

  const payload = {
    coffee_bean_id: Number(document.getElementById('coffee-bean-id').value),
    goal_type: document.getElementById('goal-type').value,
    desired_notes: document.getElementById('desired-notes').value,
    preferred_profile: document.getElementById('preferred-profile').value,
  };

  try {
    const response = await fetch(`${API_BASE}/dial-in-sessions/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });

    const data = await response.json();
    currentSessionId = data.id;
    sessionIdInput.value = currentSessionId;
    recommendationOutput.innerHTML = `<div class="muted">Session created with id ${currentSessionId}</div><pre>${JSON.stringify(data, null, 2)}</pre>`;
    await refreshSessionList();
    await refreshBrewList();
  } catch (error) {
    recommendationOutput.textContent = `Create session failed: ${error.message}`;
  }
});

brewForm.addEventListener('submit', async (event) => {
  event.preventDefault();

  if (!currentSessionId) {
    recommendationOutput.textContent = 'Create a session first.';
    return;
  }

  const payload = {
    dial_in_session_id: currentSessionId,
    dose_grams: Number(document.getElementById('dose-grams').value),
    water_grams: Number(document.getElementById('water-grams').value),
    water_temperature: Number(document.getElementById('water-temperature').value),
    grinder: 'Baratza',
    grind_setting: Number(document.getElementById('grind-setting').value),
    filter_paper: 'Hario V60',
    brew_method: 'V60',
    bloom_time_seconds: 45,
    total_brew_time_seconds: 180,
    number_of_pours: 3,
    sweetness: 7,
    acidity: 6,
    bitterness: 7,
    body: 6,
    clarity: 7,
    overall_score: Number(document.getElementById('overall-score').value),
    notes: document.getElementById('notes').value,
  };

  const response = await fetch(`${API_BASE}/brews/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });

  const data = await response.json();
  recommendationOutput.innerHTML = `<div class="muted">Brew logged successfully.</div><pre>${JSON.stringify(data, null, 2)}</pre>`;
  await refreshBrewList();
});

recommendBtn.addEventListener('click', async () => {
  if (!currentSessionId) {
    recommendationOutput.textContent = 'Create a session first.';
    return;
  }

  const response = await fetch(`${API_BASE}/dial-in-sessions/${currentSessionId}/recommendation`);
  const data = await response.json();
  recommendationOutput.innerHTML = `<div class="brew-card"><strong>Recommendation</strong><br />${data.recommendation}</div><pre>${JSON.stringify(data, null, 2)}</pre>`;
});
