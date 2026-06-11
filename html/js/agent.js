let agentData = []; // [{task_id, title, assignee, status, cron_job_id, session_id, log_tail, ...}]
let agentPanelOpen = true;
let currentAgentTaskId = null;
let loadingTimer = null;
let loadingStartTime = null;

async function loadAgents() {
  try {
    const [r, statRes] = await Promise.all([
      fetch(`${API}/api/agents`),
      fetch(`${API}/api/agents/status`),
    ]);
    agentData = await r.json();
    overlayAgentBadgesOnCards();
    loadTerminalProfiles();
  } catch (e) {
    setTerminalStatus("offline", true);
  }
}

        function getColorForString(str) {
            const palette = ['#0078d4', '#6e40c9', '#055d20', '#b35900', '#9e2a2b', '#1e40af', '#0f766e', '#86198f'];
            if (!str) return palette[0];
            let hash = 0;
            for (let i = 0; i < str.length; i++) {
                hash = str.charCodeAt(i) + ((hash << 5) - hash);
            }
            return palette[Math.abs(hash) % palette.length];
        }

        function renderAgentPanel() {
  // No-op: panel is now a terminal. Card badges still stamped by overlayAgentBadgesOnCards.
}

// Stamp robot icon badges + session list onto cards already in the DOM
function overlayAgentBadgesOnCards() {
  document.querySelectorAll(".card-agent-badge").forEach((el) => el.remove());
  document.querySelectorAll(".card-session-list").forEach((el) => el.remove());
  if (!agentData.length) return;
  agentData.forEach((a) => {
    const card = document.querySelector(`.card[data-id="${a.task_id}"]`);
    if (!card) return;
    const assignee = a.assignee || "default";
    const color = typeof getColorForString === 'function' ? getColorForString(assignee) : '#0078d4';
    const badge = document.createElement("div");
    badge.className = "card-agent-badge";
    badge.innerHTML = `<i class="ph ph-cpu" style="font-size:10px"></i> ${assignee}${a.session_id ? ' ●' : ''}`;
    badge.title = a.session_id ? `Session: ${a.session_id}` : "No session yet";
    badge.style.cssText = `
      position: absolute; bottom: 4px; right: 4px; z-index: 5;
      font-size: 10px; padding: 1px 6px; border-radius: 4px;
      background: ${color}; color: #fff; font-weight: 600; border: none;
      display: flex; align-items: center; gap: 4px; cursor: pointer;
    `;
    badge.onclick = () => {};
    card.appendChild(badge);

    // Show sessions on task card after description
    if (a.session_id) {
      const descEl = card.querySelector(".card-description");
      if (descEl) {
        const exists = card.querySelector(".card-session-list");
        if (!exists) {
          const list = document.createElement("div");
          list.className = "card-session-list";
          list.style.cssText = "display:flex;flex-wrap:wrap;gap:3px;margin-top:6px;";
          list.innerHTML = `<span class="card-badge" style="font-size:9px;background:${color};color:#fff;padding:1px 5px;border-radius:3px;display:inline-flex;align-items:center;gap:3px;"><i class="ph ph-cpu" style="font-size:8px"></i> session</span>`;
          descEl.after(list);
        }
      }
    }
  });
}

// ── Agent Config Modal ───────────────────────────────────────────────────────
function closeSessionViewerModal() {
  document.getElementById("sessionViewerModal").classList.remove("active");
}

async function openSessionViewerModal(sessionId) {
  document.getElementById("sessionViewerTitle").innerHTML =
    `<i class="ph ph-chats" style="font-size: 24px; margin-right: 8px;"></i> Session ${sessionId}`;
  const body = document.getElementById("sessionViewerBody");
  body.innerHTML = "Loading messages...";
  document.getElementById("sessionViewerModal").classList.add("active");

  try {
    const res = await fetch(`${API}/api/agents/sessions/${sessionId}/messages`);
    const data = await res.json();

    if (!res.ok || !data.messages) {
      body.innerHTML = `<span style="color:#ff7b72">Error: ${data.error || "Failed to load"}</span>`;
      return;
    }

    if (data.messages.length === 0) {
      body.innerHTML = "<em>No messages found for this session.</em>";
      return;
    }

    let html = '<div style="display:flex;flex-direction:column;gap:12px;">';
    for (const msg of data.messages) {
      const roleColor =
        msg.role === "user"
          ? "#79c0ff"
          : msg.role === "assistant"
            ? "#d2a8ff"
            : "#8b949e";
      const roleName = (msg.role || "unknown").toUpperCase();

      const formatted = formatContent(msg.content || "");
      const ts = msg.timestamp ? fmtTime(msg.timestamp * 1000) : "";
      html += `
                        <div style="border-left: 3px solid ${roleColor}; padding-left: 10px; margin-bottom: 8px;">
                            <div style="display:flex;gap:8px;align-items:baseline;font-size:11px;color:${roleColor};margin-bottom:4px;">
                                <span style="font-weight:bold;">${roleName}</span>
                                ${ts ? `<span style="opacity:0.5;font-size:10px;">${ts}</span>` : ""}
                            </div>
                            <div style="line-height:1.5; word-wrap: break-word;">${formatted}</div>
                        </div>
                    `;
    }
    html += "</div>";
    body.innerHTML = html;
  } catch (err) {
    body.innerHTML = `<span style="color:#ff7b72">Failed to fetch messages: ${err.message}</span>`;
  }
}

function switchHermesTab(tabName) {
  // Update tab buttons
  document.querySelectorAll(".hermes-tab").forEach((btn) => {
    if (btn.dataset.tab === tabName) {
      btn.classList.add("active");
      btn.style.color = "var(--primary)";
      btn.style.borderBottomColor = "var(--primary)";
    } else {
      btn.classList.remove("active");
      btn.style.color = "var(--on-surface-variant)";
      btn.style.borderBottomColor = "transparent";
    }
  });

  // Update tab content
  document.querySelectorAll(".hermes-tab-content").forEach((content) => {
    content.style.display = "none";
  });
  const targetTab = document.getElementById(
    `hermesTab${tabName.charAt(0).toUpperCase() + tabName.slice(1)}`,
  );
  if (targetTab) { targetTab.style.display = "block"; }

  // Show Save/Cancel for connection and profiles tabs
  const btnBar = document.getElementById("agentConfigBtnBar");
  if (btnBar) {
    btnBar.style.display = "flex";
  }
}

function closeAgentConfigModal() {
  document.getElementById("agentConfigModal").classList.remove("active");
}

async function openAgentConfigModal() {
  const modal = document.getElementById("agentConfigModal");

  // Open modal immediately so it feels responsive
  modal.classList.add("active");

  // Show Connection tab by default
  switchHermesTab("connection");

  // Fetch current config
  try {
    const [configRes, profilesRes, hermesStatusRes, hermesLocalRes] = await Promise.all([
      fetch(`${API}/api/agents/config`),
      fetch(`${API}/api/agents/profiles`),
      fetch(`${API}/api/agents/hermes-status`),
      fetch(`${API}/api/agents/hermes-local-config`),
    ]);
    const config = await configRes.json();
    // Merge hermes local config as defaults (only if not already set in agent config)
    if (hermesLocalRes.ok) {
      const hc = await hermesLocalRes.json();
      if (!config.provider || config.provider === "openai") config.provider = hc.provider || config.provider;
      if (!config.base_url) config.base_url = hc.base_url || "";
      if (!config.api_key) config.api_key = hc.api_key || "";
      if (!config.model) config.model = hc.model || "";
    }
    let profiles = ["default"];
    if (profilesRes.ok) {
      profiles = await profilesRes.json();
    }

    // Display Hermes connection status banner
    if (hermesStatusRes.ok) {
      const hermesStatus = await hermesStatusRes.json();
      updateHermesStatusBanner(hermesStatus, config.execution_mode || "local");
    }

    // Populate project target dropdown removed

    const modeRadios = document.getElementsByName("hermesConnectionMode");
    for (let r of modeRadios) {
      if (r.value === (config.execution_mode || "local")) r.checked = true;
    }

    // Show/hide remote URL based on mode
    toggleConnectionMode();

    document.getElementById("hermesRemoteUrl").value = config.remote_url || "";

    // Populate provider/model settings
    const providerVal = config.provider || "openai";
    document.getElementById("providerSelect").value = providerVal;
    onProviderChange();
    if (config.base_url) {
      document.getElementById("providerBaseUrl").value = config.base_url;
    }
    const apiKeyInput = document.getElementById("providerApiKey");
    apiKeyInput.value = config.api_key || "";
    apiKeyInput.type = "password";
    document.getElementById("apiKeyToggleIcon").className = "ph ph-eye";
    if (config.model) {
      document.getElementById("modelSelect").value = config.model;
    }
    if (config.model) {
      const status = document.getElementById("modelFetchStatus");
      status.textContent = `Model: ${config.model}`;
    }

    // Display available profiles
    renderProfileList(profiles);

    const profileSelect = document.getElementById("hermesDefaultProfile");
    profileSelect.innerHTML = "";
    profiles.forEach((p) => {
      const opt = document.createElement("option");
      opt.value = p;
      opt.textContent = p;
      profileSelect.appendChild(opt);
    });
    profileSelect.value =
      config.default_profile ||
      (profiles.includes("default") ? "default" : profiles[0]);

    // Build category mapping UI
    renderCategoryProfileMapping(config.category_profile_map || {}, profiles);
  } catch (err) {
    console.error("Failed to load agent config", err);
  }
}

function updateHermesStatusBanner(hermesStatus, mode) {
  const banner = document.getElementById("hermesStatusBanner");
  const icon = document.getElementById("hermesStatusIcon");
  const text = document.getElementById("hermesStatusText");
  const detail = document.getElementById("hermesStatusDetail");

  const available = hermesStatus.available;
  const isRemote = hermesStatus.mode === "remote" || mode === "remote";

  // Update system info panel
  document.getElementById("hermesInfoPlatform").textContent = hermesStatus.platform || "—";
  document.getElementById("hermesInfoMode").textContent = hermesStatus.mode || mode || "—";
  document.getElementById("hermesInfoUrl").textContent = hermesStatus.url || hermesStatus.path || "—";
  document.getElementById("hermesInfoProfiles").textContent = hermesStatus.profiles != null ? String(hermesStatus.profiles) : "—";

  if (available) {
    banner.style.background = "rgba(63, 185, 80, 0.1)";
    banner.style.border = "1px solid rgba(63, 185, 80, 0.3)";
    icon.innerHTML = '<i class="ph-fill ph-check-circle" style="font-size: 24px; color: #3fb950;"></i>';
    if (isRemote) {
      text.textContent = "Connected to Hermes Gateway";
      text.style.color = "#3fb950";
      const ses = hermesStatus.sessions != null ? ` · ${hermesStatus.sessions} sessions` : '';
      detail.textContent = `${hermesStatus.url}${ses}`;
    } else {
      text.textContent = "Hermes CLI Available";
      text.style.color = "#3fb950";
      const ver = hermesStatus.version ? ` v${hermesStatus.version}` : '';
      detail.textContent = `${hermesStatus.path || 'Found in PATH'}${ver}`;
    }
    detail.style.color = "var(--on-surface-variant)";
  } else {
    banner.style.background = "rgba(248, 81, 73, 0.1)";
    banner.style.border = "1px solid rgba(248, 81, 73, 0.3)";
    icon.innerHTML = '<i class="ph-fill ph-x-circle" style="font-size: 24px; color: #f85149;"></i>';
    if (isRemote) {
      text.textContent = "Gateway Unreachable";
      text.style.color = "#f85149";
      detail.textContent = hermesStatus.error || `Cannot reach ${hermesStatus.url || 'remote URL'}`;
    } else {
      text.textContent = "Hermes CLI Not Found";
      text.style.color = "#f85149";
      detail.textContent = hermesStatus.error || 'Install Hermes or switch to Remote mode';
    }
    detail.style.color = "var(--on-surface-variant)";
  }
}

function renderProfileList(profiles) {
  const container = document.getElementById("hermesProfileList");
  const count = document.getElementById("hermesProfileCount");
  count.textContent = `(${profiles.length})`;

  container.innerHTML = profiles
    .map((p) => {
      const color = typeof getColorForString === 'function' ? getColorForString(p) : '#0078d4';
      return `<span style="font-size:11px;padding:4px 10px;border-radius:4px;background:${color};color:#fff;font-weight:600;">${p}</span>`;
    })
    .join("");
}

function applyHermesUrlPreset() {
  const preset = document.getElementById("hermesRemoteUrlPreset").value;
  if (preset) {
    document.getElementById("hermesRemoteUrl").value = preset;
  }
}

function toggleConnectionMode() {
  const mode =
    document.querySelector('input[name="hermesConnectionMode"]:checked')
      ?.value || "local";
  const remoteContainer = document.getElementById("hermesRemoteUrlContainer");
  remoteContainer.style.display = mode === "remote" ? "block" : "none";
}

function onProviderChange() {
  const val = document.getElementById("providerSelect").value;
  const baseUrlContainer = document.getElementById("baseUrlContainer");
  const baseUrlInput = document.getElementById("providerBaseUrl");
  const status = document.getElementById("modelFetchStatus");
  const modelSelect = document.getElementById("modelSelect");

  if (val === "custom") {
    baseUrlContainer.style.display = "block";
    if (!baseUrlInput.value) baseUrlInput.placeholder = "https://your-api.com/v1";
  } else if (val === "ollama") {
    baseUrlContainer.style.display = "block";
    if (!baseUrlInput.value) {
      baseUrlInput.value = "http://localhost:11434/v1";
    }
    baseUrlInput.placeholder = "http://localhost:11434/v1";
  } else if (val === "azure") {
    baseUrlContainer.style.display = "block";
    baseUrlInput.placeholder = "https://RESOURCE.openai.azure.com";
  } else {
    baseUrlContainer.style.display = "none";
  }
  status.textContent = "";
  modelSelect.innerHTML = '<option value="">— select model —</option>';
}

function toggleApiKey() {
  const input = document.getElementById("providerApiKey");
  const icon = document.getElementById("apiKeyToggleIcon");
  if (input.type === "password") {
    input.type = "text";
    icon.className = "ph ph-eye-slash";
  } else {
    input.type = "password";
    icon.className = "ph ph-eye";
  }
}

async function fetchModels(event) {
  const btn = event?.currentTarget || document.querySelector("button[title='Fetch models from provider API']");
  if (btn) btn.disabled = true;
  const status = document.getElementById("modelFetchStatus");
  const select = document.getElementById("modelSelect");
  const apiKey = document.getElementById("providerApiKey").value.trim();
  const baseUrl = document.getElementById("providerBaseUrl").value.trim();
  const provider = document.getElementById("providerSelect").value;

  if (!apiKey && provider !== "ollama" && provider !== "custom") {
    status.textContent = "API key recommended (some custom endpoints may allow empty)";
    // We don't return early, custom might not need a key
  }

  status.textContent = "Fetching models...";
  status.style.color = "var(--on-surface-variant)";

  try {
    const res = await fetch(`${API}/api/agents/models`, {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({ provider, base_url: baseUrl, api_key: apiKey })
    });
    const data = await res.json();

    if (data.error) {
      status.textContent = `Error: ${data.error}`;
      status.style.color = "#f85149";
      select.innerHTML = '<option value="">— fetch failed —</option>';
    } else if (data.models && data.models.length > 0) {
      const current = select.value;
      select.innerHTML = '<option value="">— select model —</option>' +
        data.models.map(m => `<option value="${escHtml(m)}">${escHtml(m)}</option>`).join("");
      if (data.models.includes(current)) {
        select.value = current;
      }
      status.textContent = `${data.models.length} models loaded`;
      status.style.color = "#3fb950";
    } else {
      status.textContent = "No models returned";
      status.style.color = "var(--on-surface-variant)";
    }
  } catch (e) {
    status.textContent = `Request failed: ${e.message}`;
    status.style.color = "#f85149";
  } finally {
    if (btn) btn.disabled = false;
  }
}

async function refreshHermesStatus() {
  const btn = document.getElementById("hermesRefreshBtn");
  const originalHTML = btn.innerHTML;
  btn.innerHTML = '<i class="ph ph-spinner" style="font-size:14px;animation:spin 1s linear infinite"></i>';
  btn.disabled = true;

  try {
    const res = await fetch(`${API}/api/agents/hermes-status`);
    const status = await res.json();
    const mode =
      document.querySelector('input[name="hermesConnectionMode"]:checked')
        ?.value || "local";
    updateHermesStatusBanner(status, mode);
    showToast(
      status.available ? "Hermes reachable" : "Hermes not available",
      status.available ? "success" : "error",
    );
  } catch (err) {
    showToast("Refresh failed", "error");
  } finally {
    btn.innerHTML = originalHTML;
    btn.disabled = false;
  }
}

async function refreshHermesSessions() {
  const container = document.getElementById("hermesSessionsList");
  const countEl = document.getElementById("sessionsCount");
  const gatewayEl = document.getElementById("sessionsGateway");
  container.innerHTML =
    '<div style="text-align:center;padding:20px;color:var(--on-surface-variant);"><i class="ph ph-spinner" style="animation:spin 1s linear infinite;"></i> Loading sessions...</div>';

  try {
    const res = await fetch(`${API}/api/agents/sessions`);
    const data = await res.json();

    if (data.gateway) {
      gatewayEl.textContent = data.gateway;
    } else if (data.fallback) {
      gatewayEl.textContent = "cached";
    } else {
      gatewayEl.textContent = "";
    }

    if (!data.sessions || data.sessions.length === 0) {
      countEl.textContent = "";
      container.innerHTML = `
                        <div class="sessions-empty">
                            <i class="ph ph-terminal-window"></i>
                            <div style="font-size:14px;margin-bottom:6px;">No sessions found</div>
                            <div style="font-size:12px;opacity:0.7;">Start a Hermes CLI session to see it here</div>
                        </div>`;
      return;
    }

    // Sort by last_active descending (newest first)
    data.sessions.sort((a, b) => (b.last_active || 0) - (a.last_active || 0));

    countEl.textContent = `(${data.sessions.length})`;
    container.classList.add("cli-terminal");

    let html = `
                    <div class="cli-terminal-header">
                        <div class="cli-terminal-col cli-col-id">ID</div>
                        <div class="cli-terminal-col cli-col-active">Last Accessed</div>
                        <div class="cli-terminal-col cli-col-preview">Preview</div>
                        <div class="cli-terminal-col cli-col-action"></div>
                    </div>
                `;

    html += data.sessions
      .map((s) => {
        const isActive = s.is_active;
        const preview = s.preview || "";

        // compute relative time
        let activeStr = s.last_active_fmt || s.started_at_fmt || "";
        if (s.last_active) {
          const seconds = Math.floor(Date.now() / 1000 - s.last_active);
          if (seconds < 60) activeStr = "just now";
          else if (seconds < 3600)
            activeStr = Math.floor(seconds / 60) + "m ago";
          else if (seconds < 86400)
            activeStr = Math.floor(seconds / 3600) + "h ago";
          else if (seconds < 172800) activeStr = "yesterday";
          else activeStr = Math.floor(seconds / 86400) + "d ago";
        }

        const dot = isActive
          ? '<span class="cli-active-dot" title="Active">●</span> '
          : '<span class="cli-active-dot" style="opacity:0"> </span> ';
        const cost = s.estimated_cost_usd;
        const costStr =
          cost != null && cost > 0 ? `\nCost: $${cost.toFixed(4)}` : "";
        const tooltip = `Model: ${s.model || "—"}${costStr}`;

        return `
                        <div class="cli-terminal-row" title="${escHtml(tooltip)}">
                            <div class="cli-terminal-col cli-col-id" onclick="openSessionViewerModal('${escHtml(s.id)}')">${dot}<span style="font-size:10px;">${escHtml(s.id)}</span></div>
                            <div class="cli-terminal-col cli-col-active" onclick="openSessionViewerModal('${escHtml(s.id)}')">${escHtml(activeStr)}</div>
                            <div class="cli-terminal-col cli-col-preview" onclick="openSessionViewerModal('${escHtml(s.id)}')">${escHtml(preview)}</div>
                            <div class="cli-terminal-col cli-col-action" style="display:flex;gap:4px;align-items:center;">
                                <button class="btn" style="font-size:10px;padding:2px 6px;" onclick="event.stopPropagation();resumeSession('${escHtml(s.id)}')">Resume</button>
                                <button class="btn" style="font-size:10px;padding:2px 6px;border-color:#f85149;color:#f85149;" onclick="event.stopPropagation();endSession('${escHtml(s.id)}')">End</button>
                                <button class="agent-sync-btn" style="font-size:10px;padding:2px 6px;" onclick="event.stopPropagation();deleteSession('${escHtml(s.id)}')" title="Delete"><i class="ph ph-trash" style="font-size:10px;"></i></button>
                            </div>
                        </div>`;
      })
      .join("");

    container.innerHTML = html;
  } catch (err) {
    container.innerHTML =
      '<div class="sessions-empty"><i class="ph-fill ph-warning"></i><div style="font-size:14px;">Failed to load sessions</div><div style="font-size:12px;opacity:0.7;">' +
      (err.message || "API unreachable") +
      "</div></div>";
  }
}

function escHtml(str) {
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function renderCategoryProfileMapping(mapping, profiles) {
    const container = document.getElementById('hermesProfileMapContainer');
    
    let categories = [];
    if (window.allTasks) {
        categories = [...new Set(window.allTasks.map(t => (t.category || '').toUpperCase().trim()).filter(Boolean))].sort();
    }
    if (categories.length === 0) {
        categories = ['CORE', 'BACKEND', 'CLIENT', 'UI'];
    }

    // Auto-assign profiles round-robin when no mapping exists
    const nonDefaultProfiles = profiles.filter(p => p !== 'default');
    if (Object.keys(mapping).length === 0 && nonDefaultProfiles.length > 0) {
        categories.forEach((cat, i) => {
            mapping[cat] = nonDefaultProfiles[i % nonDefaultProfiles.length];
        });
    }

    container.innerHTML = `
        <div style="display:grid;grid-template-columns:repeat(auto-fill, minmax(200px, 1fr));gap:12px;">
            ${categories.map(cat => {
                const selected = mapping[cat] || '';
                const catColor = typeof getColorForString === 'function' ? getColorForString(cat) : '#888';
                return `
                    <div style="background:var(--surface-variant);border:1px solid var(--border-color);border-radius:8px;padding:14px;display:flex;flex-direction:column;gap:10px;transition:border-color 0.2s;">
                        <div style="display:flex;align-items:center;gap:8px;">
                            <div style="width:14px;height:14px;border-radius:4px;background:${catColor}"></div>
                            <span style="font-size:13px;font-weight:600;color:var(--on-surface)">${cat}</span>
                        </div>
                        <select class="form-input profile-map-select" data-category="${cat}" style="width:100%;font-size:12px;border-radius:6px;">
                            <option value="">(default)</option>
                            ${profiles.map(p => `<option value="${p}" ${p === selected ? 'selected' : ''} style="${typeof getColorForString === 'function' ? 'color:' + getColorForString(p) : ''}">${p}</option>`).join('')}
                        </select>
                    </div>
                `;
            }).join('')}
        </div>
    `;
}

async function saveAgentConfig() {
  const modeRadios = document.getElementsByName("hermesConnectionMode");
  let mode = "local";
  for (let r of modeRadios) {
    if (r.checked) mode = r.value;
  }

  // Build profile map from selectors
  const profileMap = {};
  document.querySelectorAll(".profile-map-select").forEach((sel) => {
    const cat = sel.dataset.category;
    const prof = sel.value;
    if (prof) profileMap[cat] = prof;
  });

  const config = {
    execution_mode: mode,
    remote_url: document.getElementById("hermesRemoteUrl").value,
    default_profile: document.getElementById("hermesDefaultProfile").value,
    category_profile_map: profileMap,
    provider: document.getElementById("providerSelect").value,
    base_url: document.getElementById("providerBaseUrl").value,
    api_key: document.getElementById("providerApiKey").value,
    model: document.getElementById("modelSelect").value,
  };

  try {
    await fetch(`${API}/api/agents/config`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(config),
    });
    closeAgentConfigModal();
    loadAgents(); // Reload agents to reflect any changes if needed
  } catch (err) {
    console.error("Failed to save config", err);
    alert("Failed to save configuration");
  }
}

// Open agent detail modal
async function openAgentModal(taskId) {
  // Modal removed — no-op
  return;
}

function closeAgentModal() {
  // Modal removed — no-op
}

async function triggerAgent(taskId) {
  try {
    const r = await fetch(`${API}/api/agents/${taskId}/trigger`, {
      method: "POST",
    });
    const d = await r.json();
    showToast(
      d.success ? `Agent triggered for #${taskId}` : `Error: ${d.error}`,
      d.success ? "success" : "error",
    );
    if (d.success) setTimeout(() => refreshAgentLog(taskId), 3000);
  } catch (e) {
    showToast("API unreachable", "error");
  }
}

async function toggleCron(taskId, hasCron) {
  const action = hasCron ? 'disable' : 'enable';
  try {
    const r = await fetch(`${API}/api/agents/${taskId}/cron/${action}`, {
      method: "POST",
    });
    const d = await r.json();
    showToast(
      d.success ? `Cron ${action}d for #${taskId}` : `Error: ${d.error}`,
      d.success ? "success" : "error",
    );
    if (d.success) {
      setTimeout(() => {
        loadAgentData();
      }, 1000);
    }
  } catch (e) {
    showToast("API unreachable", "error");
  }
}

async function refreshAgentLog(taskId) {
  const lb = document.getElementById("agentLogBox");
  if (!lb) return;
  try {
    const r = await fetch(`${API}/api/agents/${taskId}/log`);
    const d = await r.json();
    lb.innerHTML = d.log
      ? d.log
          .replace(/&/g, "&amp;")
          .replace(/</g, "&lt;")
          .replace(/>/g, "&gt;")
          .replace(/DONE/g, '<span class="log-done">DONE</span>')
      : "<em>Empty log.</em>";
    lb.scrollTop = lb.scrollHeight;
  } catch (e) {}
}

async function reassignAgent(taskId) {
  let profiles = ['default'];
  try {
    const r = await fetch(`${API}/api/agents/profiles`);
    if (r.ok) profiles = await r.json();
  } catch (e) {}
  const profile = prompt(`Assign to profile (options: ${profiles.join(', ')}):`);
  if (!profile) return;
  try {
    const r = await fetch(`${API}/api/agents/${taskId}/assign`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ profile }),
    });
    const d = await r.json();
    showToast(
      d.success ? `#${taskId} → ${profile}` : `Error: ${d.error}`,
      d.success ? "success" : "error",
    );
    if (d.success) {
      await loadAgents();
      openAgentModal(taskId);
    }
  } catch (e) {
    showToast("API unreachable", "error");
  }
}

async function triggerSync() {
  const btn = document.getElementById("agentSyncBtn");
  btn.textContent = "…";
  btn.disabled = true;
  try {
    const r = await fetch(`${API}/api/agents/sync`, { method: "POST" });
    const d = await r.json();
    showToast(
      d.success
        ? "Agent sync complete"
        : `Sync error: ${d.output?.slice(0, 80)}`,
      d.success ? "success" : "error",
    );
    await loadAgents();
  } catch (e) {
    showToast("Sync API unreachable", "error");
  } finally {
    btn.innerHTML =
      '<i class="ph ph-arrows-clockwise" style="font-size: 12px;"></i> Sync';
    btn.disabled = false;
  }
}

async function triggerIndex() {
  const btn = document.getElementById("agentIndexBtn");
  btn.textContent = "…";
  btn.disabled = true;
  try {
    const r = await fetch(`${API}/api/agents/index`, { method: "POST" });
    const d = await r.json();
    if (d.success) {
      showToast(
        "Task index rebuilt — related tasks + priority scores updated",
        "success",
      );
    } else {
      showToast(`Index error: ${(d.output || "").slice(0, 100)}`, "error");
      console.error("Index output:", d.output);
    }
  } catch (e) {
    showToast("Index API unreachable", "error");
  } finally {
    btn.innerHTML =
      '<i class="ph ph-squares-four" style="font-size: 12px;"></i> Index';
    btn.disabled = false;
  }
}
async function toggleDaemon() {
  const btn = document.getElementById("agentDaemonBtn");
  const isRunning = btn.dataset.running === "true";
  btn.disabled = true;
  try {
    const action = isRunning ? "stop" : "start";
    await fetch(`${API}/api/agents/daemon/${action}`, { method: "POST" });
    showToast(`Daemon ${isRunning ? "stopped" : "started"}`, "success");
    loadAgents(); // Reload to update UI
  } catch (e) {
    showToast("Failed to toggle daemon", "error");
  } finally {
    btn.disabled = false;
  }
}

// ── Terminal (multi-session tabs) ──────────────────────────────────────
let terminalTabs = [];
let terminalActiveTab = -1;
let terminalSending = false;
let tabCounter = 0;

function escHtml(s) {
  if (typeof s !== "string") return "";
  const d = document.createElement("div");
  d.textContent = s;
  return d.innerHTML;
}

function formatContent(text) {
  text = escHtml(text);
  text = text.replace(/\\n/g, "\n");
  const blocks = [];
  let lastIdx = 0;
  const codeRegex = /```(\w*)\n?([\s\S]*?)```/g;
  let match;
  while ((match = codeRegex.exec(text)) !== null) {
    if (match.index > lastIdx) {
      blocks.push({ type: "text", content: text.slice(lastIdx, match.index) });
    }
    const lang = match[1] ? escHtml(match[1]) : "";
    const code = escHtml(match[2]);
    blocks.push({ type: "code", lang, code });
    lastIdx = match.index + match[0].length;
  }
  if (lastIdx < text.length) {
    blocks.push({ type: "text", content: text.slice(lastIdx) });
  }
  return blocks.map(b => {
    if (b.type === "code") {
      const langTag = b.lang ? `<span style="font-size:10px;color:#8b949e;display:block;margin-bottom:4px;">${b.lang}</span>` : "";
      return `<div style="background:#161b22;border:1px solid #30363d;border-radius:6px;padding:12px;margin:8px 0;overflow-x:auto;font-family:ui-monospace,SFMono-Regular,SF Mono,Menlo,Consolas,monospace;font-size:12px;line-height:1.5;color:#e6edf3;white-space:pre;">${langTag}<code style="background:none;padding:0;color:#e6edf3;white-space:pre;">${b.code}</code></div>`;
    }
    let content = b.content.replace(/\n/g, "<br>");
    content = content.replace(/`([^`]+)`/g, '<code style="background:#161b22;padding:1px 4px;border-radius:3px;font-size:12px;color:#f97583;">$1</code>');
    return content;
  }).join("");
}

function termMsg(containerId, role, content, labelOverride) {
  const body = document.getElementById(containerId);
  if (!body) return;
  const ts = fmtTime(Date.now());
  const roleColor =
    role === "user" ? "#79c0ff"
      : role === "assistant" ? "#d2a8ff"
        : role === "error" ? "#f85149"
          : role === "info" ? "#8b949e" : "#c9d1d9";
  const roleName = labelOverride || ({ user: "You", assistant: "Hermes", error: "Error", info: "System" }[role] || role || "Unknown");
  const formatted = formatContent(content || "");
  const div = document.createElement("div");
  div.style.cssText = "padding:4px 0;";
  div.innerHTML = `
    <div style="border-left:3px solid ${roleColor};padding-left:10px;">
      <div style="display:flex;gap:8px;align-items:baseline;font-size:11px;color:${roleColor};margin-bottom:2px;">
        <span style="font-weight:bold;">${roleName}</span>
        <span style="opacity:0.5;font-size:10px;">${ts}</span>
      </div>
      <div style="font-size:13px;line-height:1.5;word-wrap:break-word;">${formatted}</div>
    </div>`;
  body.appendChild(div);
  body.scrollTop = body.scrollHeight;
}

// ── localStorage persistence ──────────────────────────────────────────
function saveTerminalState() {
  try {
    const data = { tabs: terminalTabs, tabCounter, terminalActiveTab };
    localStorage.setItem("talariaTerminalTabs", JSON.stringify(data));
  } catch (e) { /* quota exceeded, ignore */ }
}

function restoreTerminalState() {
  try {
    const raw = localStorage.getItem("talariaTerminalTabs");
    if (!raw) return false;
    const data = JSON.parse(raw);
    if (!data.tabs || !data.tabs.length) return false;
    terminalTabs = data.tabs.map(t => ({
      ...t,
      localSessionId: null,
      status: "stale",
      messages: (t.messages || []).map(m => ({
        ...m,
        content: m.content || ""
      }))
    }));
    tabCounter = data.tabCounter || 0;
    terminalActiveTab = data.terminalActiveTab || 0;
    if (terminalActiveTab >= terminalTabs.length) terminalActiveTab = 0;
    return true;
  } catch (e) { return false; }
}

function fmtTime(ts) {
  const d = new Date(ts);
  const hh = String(d.getHours()).padStart(2, "0");
  const mm = String(d.getMinutes()).padStart(2, "0");
  const dd = String(d.getDate()).padStart(2, "0");
  const mo = String(d.getMonth() + 1).padStart(2, "0");
  const yyyy = d.getFullYear();
  return `${hh}:${mm} - ${dd}.${mo}.${yyyy}`;
}

// Normalize task ID: #000, #00, #0, 000, 00, 0 → padded 3-digit
function normalizeTaskId(raw) {
  if (!raw) return "";
  let id = raw.replace(/^#+/, "").trim();
  if (/^\d+$/.test(id)) return id.padStart(3, "0");
  return id;
}

// Nav suggestions with arrow keys + Enter; Enter also sends msg when no suggestions
document.addEventListener("keydown", e => {
  if (e.target.id !== "terminalInlineInput") return;
  if (e.key === "Enter") sendTerminalInline();
});

// Hide suggestions on blur
document.addEventListener("click", e => {
  const suggest = document.getElementById("terminalCmdSuggest");
  if (suggest && !e.target.closest("#terminalInlineInput, #terminalCmdSuggest")) {
    suggest.style.display = "none";
  }
});
function renderTerminalTabs() {
  const list = document.getElementById("terminalTabList");
  if (!list) return;
  const idFn = t => t.title || t.hermesSessionId || t.localSessionId || `tab:${t.tabNum}`;
  list.innerHTML = terminalTabs.map((t, i) => {
    const active = i === terminalActiveTab ? "active" : "";
    const dot = t.localSessionId ? "● " : (t.status === "stale" ? "○ " : "");
    const msgCount = t.messages && t.messages.length > 0 ? ` <span style="opacity:0.4;font-size:9px;">${t.messages.length}</span>` : "";
    return `<div class="term-tab ${active}" onclick="switchTerminalTab(${i})">
      ${dot}${escHtml(idFn(t))}${msgCount}
      <span class="term-tab-close" onclick="event.stopPropagation();closeTerminalTab(${i})" title="Stop & close">✕</span>
    </div>`;
  }).join("");
  saveTerminalState();
}

function showTerminalMessages() {
  const body = document.getElementById("terminalMessages");
  if (!body) return;
  body.innerHTML = "";
  if (terminalActiveTab < 0 || terminalActiveTab >= terminalTabs.length) return;
  const tab = terminalTabs[terminalActiveTab];
  const profileLabel = tab.profile && tab.profile !== "default" ? tab.profile : "Hermes";
  for (const m of tab.messages) {
    if (!m.ts) m.ts = Date.now();
    const ts = fmtTime(m.ts);
    const div = document.createElement("div");
    div.style.cssText = "padding:4px 0;";
    const roleColor =
      m.role === "user" ? "#79c0ff"
        : m.role === "assistant" ? "#d2a8ff"
          : m.role === "error" ? "#f85149"
            : (m.role === "info" || m.role === "loading") ? "#8b949e" : "#c9d1d9";
    const roleName = m.role === "assistant" ? (m.label || profileLabel)
      : ({ user: "You", error: "Error", info: "System", loading: "System" }[m.role] || m.role || "Unknown");
    let formatted = formatContent(m.content || "");
    if (m.role === "loading") {
      formatted = `<span class="ascii-loader"></span> ` + formatted;
    }
    div.innerHTML = `
      <div style="border-left:3px solid ${roleColor};padding-left:10px;">
        <div style="display:flex;gap:8px;align-items:baseline;font-size:11px;color:${roleColor};margin-bottom:2px;">
          <span style="font-weight:bold;">${roleName}</span>
          <span style="opacity:0.5;font-size:10px;">${ts}</span>
        </div>
        <div style="font-size:13px;line-height:1.5;word-wrap:break-word;">${formatted}</div>
      </div>`;
    body.appendChild(div);
  }
  if (tab.status === "stale" && tab.hermesSessionId && tab.messages.length > 0) {
    const restoreBanner = document.createElement("div");
    restoreBanner.style.cssText = "padding:8px;text-align:center;border-bottom:1px solid var(--border-color);margin-bottom:8px;";
    restoreBanner.innerHTML = `
      <div style="font-size:11px;color:var(--on-surface-variant);margin-bottom:4px;">Session has ${tab.messages.length} saved messages</div>
      <button class="btn" style="font-size:10px;padding:3px 8px;" onclick="addTerminalTabWithResume('${escHtml(tab.hermesSessionId)}')">Restore session</button>
    `;
    body.appendChild(restoreBanner);
  }
  body.scrollTop = body.scrollHeight;
  const input = document.getElementById("terminalInlineInput");
  if (tab.status === "stale") {
    input.disabled = true;
    input.placeholder = "Session expired — restore above";
  } else {
    input.disabled = !tab.localSessionId;
    input.placeholder = tab.localSessionId ? "Type a message and press Enter..." : "Start a session first...";
  }
  updateTerminalHeader();
  if (typeof update2DWorld === "function") {
    update2DWorld();
  }
  _hookTypingDetection();
}

function updateTerminalHeader() {
  const tab = terminalTabs[terminalActiveTab];
  const dot = document.getElementById("terminalStatusDot");
  const label = document.getElementById("terminalStatusLabel");
  const taskChip = document.getElementById("terminalTaskChip");
  if (!tab) {
    if (dot) dot.style.background = "#888";
    if (label) label.textContent = "disconnected";
    if (taskChip) taskChip.style.display = "none";
    return;
  }
  if (tab.status === "stale") { if (dot) dot.style.background = "#f0883e"; if (label) label.textContent = "stale (reload)"; return; }
  if (!tab.localSessionId) { if (dot) dot.style.background = "#888"; if (label) label.textContent = "disconnected"; return; }
  if (dot) dot.style.background = "#3fb950";
  if (label) label.textContent = [tab.profile, tab.model].filter(Boolean).join(" · ") || "connected";
  if (taskChip) {
    if (tab.taskId) {
      taskChip.style.display = "inline-flex";
      taskChip.innerHTML = `<i class="ph ph-cpu" style="font-size:10px"></i> #${escHtml(tab.taskId)}`;
    } else {
      taskChip.style.display = "none";
    }
  }
}

async function loadTerminalProfiles() {
  const sel = document.getElementById("terminalProfileSelectInline");
  if (!sel) return;
  try {
    const res = await fetch(`${API}/api/agents/terminal/profiles`);
    const profiles = await res.json();
    sel.innerHTML = profiles.map(p => `<option value="${p}">${p}</option>`).join("");
    const modalSel = document.getElementById("terminalProfileSelect");
    if (modalSel) modalSel.innerHTML = sel.innerHTML;
    // Spawn avatars for all available profiles immediately
    _spawnProfileAvatars(profiles);
  } catch (e) {
    sel.innerHTML = '<option value="default">default</option>';
    _spawnProfileAvatars(['default']);
  }
}

// ── Tab lifecycle ─────────────────────────────────────────────────────
function addTerminalTab() {
  const profile = document.getElementById("terminalProfileSelectInline").value;
  const modelInput = document.getElementById("terminalModelInline");
  const model = modelInput ? modelInput.value.trim() || null : null;
  tabCounter++;
  const tab = { tabNum: tabCounter, localSessionId: null, hermesSessionId: null,
    profile, model, messages: [], status: "new", taskId: null };
  terminalTabs.push(tab);
  terminalActiveTab = terminalTabs.length - 1;
  renderTerminalTabs();
  showTerminalMessages();
  startTerminalSession(tab);
}

async function startTerminalSession(tab) {
  if (!tab) tab = terminalTabs[terminalActiveTab];
  if (!tab) return;
  tab.messages.push({ role: "info", content: `Starting session (${tab.profile})...` });
  showTerminalMessages();
  try {
    // Get backend from saved config
    let backend = 'hermes-agent';
    try {
      const cfgRes = await fetch(`${API}/api/agents/terminal/config`);
      if (cfgRes.ok) {
        const cfg = await cfgRes.json();
        if (cfg.backend) backend = cfg.backend;
      }
    } catch (e) { /* use default */ }

    const requestBody = {
      profile: tab.profile,
      task_id: tab.taskId,
      project: tab.project,
      model: tab.model,
      backend: backend
    };
    if (tab.taskId) {
      requestBody.title = `talaria-task-${tab.taskId}`;
    }
    const res = await fetch(`${API}/api/agents/terminal/start`, {
      method: "POST", headers: {"Content-Type": "application/json"},
      body: JSON.stringify(requestBody)
    });
    const data = await res.json();
    tab.localSessionId = data.id;
    tab.hermesSessionId = data.hermes_session_id;
    tab.model = data.model;
    tab.status = "connected";
    tab.messages.push({ role: "info", content: `Session ready (${data.hermes_session_id || data.id})` });
    renderTerminalTabs();
    showTerminalMessages();
    document.getElementById("terminalInlineInput").focus();
  } catch (e) {
    tab.messages.push({ role: "error", content: `Failed: ${e.message}` });
    tab.status = "error";
    showTerminalMessages();
  }
}

async function reconnectTerminalTab(idx) {
  const tab = terminalTabs[idx];
  if (!tab) return;
  tab.status = "new";
  tab.localSessionId = null;
  tab.messages.push({ role: "info", content: `Reconnecting (${tab.profile})...` });
  showTerminalMessages();
  try {
    if (tab.hermesSessionId) {
      const newIdx = terminalTabs.length;
      await addTerminalTabWithResume(tab.hermesSessionId);
      await closeTerminalTab(idx);
      terminalActiveTab = Math.min(newIdx, terminalTabs.length - 1);
      renderTerminalTabs();
      showTerminalMessages();
      return;
    }
    const res = await fetch(`${API}/api/agents/terminal/start`, {
      method: "POST", headers: {"Content-Type": "application/json"},
      body: JSON.stringify({profile: tab.profile})
    });
    const data = await res.json();
    tab.localSessionId = data.id;
    tab.hermesSessionId = data.hermes_session_id;
    tab.model = data.model;
    tab.status = "connected";
    const modelInfo = data.model ? ` · ${data.model}` : "";
    tab.messages.push({ role: "info", content: `Reconnected${modelInfo} (${data.hermes_session_id || data.id})` });
    renderTerminalTabs();
    showTerminalMessages();
    document.getElementById("terminalInlineInput").focus();
  } catch (e) {
    tab.messages.push({ role: "error", content: `Reconnect failed: ${e.message}` });
    tab.status = "error";
    showTerminalMessages();
  }
}

function switchTerminalTab(idx) {
  if (idx < 0 || idx >= terminalTabs.length) return;
  terminalActiveTab = idx;
  renderTerminalTabs();
  showTerminalMessages();
    update2DWorld();
}

async function closeTerminalTab(idx) {
  const tab = terminalTabs[idx];
  if (tab && tab.localSessionId) {
    await fetch(`${API}/api/agents/terminal/${tab.localSessionId}/stop`, {method: "POST"}).catch(() => {});
    await fetch(`${API}/api/agents/terminal/${tab.localSessionId}/delete`, {method: "POST"}).catch(() => {});
  }
  terminalTabs.splice(idx, 1);
  if (terminalActiveTab >= terminalTabs.length) terminalActiveTab = terminalTabs.length - 1;
  if (terminalActiveTab < 0 && terminalTabs.length > 0) terminalActiveTab = 0;
  renderTerminalTabs();
  showTerminalMessages();
  if (terminalTabs.length === 0) {
    document.getElementById("terminalMessages").innerHTML =
      '<div style="padding:16px;color:var(--on-surface-variant);text-align:center;">Press <strong>+ New</strong> to start a terminal session.</div>';
    document.getElementById("terminalInlineInput").disabled = true;
    document.getElementById("terminalInlineInput").placeholder = "Start session first...";
    updateTerminalHeader();
  }
}

// ── Send / Chat ────────────────────────────────────────────────────────
async function sendTerminalInline() {
  const input = document.getElementById("terminalInlineInput");
  const msg = input.value.trim();
  const tab = terminalTabs[terminalActiveTab];
  if (!msg || !tab || !tab.localSessionId || terminalSending) return;

  if (msg === "/help" || msg === "/") {
    showHelp(tab);
    input.value = "";
    return;
  }
  const taskMatch = msg.match(/^\/task(?:\s+(.+))?/i);
  if (taskMatch) {
    if (taskMatch[1]) {
      const rawId = taskMatch[1].trim();
      const taskId = normalizeTaskId(rawId);
      const oldSessionId = tab.localSessionId;
      tab.taskId = taskId;
      tab.messages.push({ role: "info", content: `Task context set to #${taskId}` });
      showTerminalMessages();
      input.value = "";
      if (oldSessionId) {
        tab.messages.push({ role: "info", content: `Restarting session with task context...` });
        showTerminalMessages();
        fetch(`${API}/api/agents/terminal/${oldSessionId}/stop`, {method: "POST"}).catch(() => {});
        tab.localSessionId = null;
        tab.hermesSessionId = null;
        tab.status = "new";
        startTerminalSession(tab);
      }
    } else {
      tab.messages.push({ role: "info", content: `Current Task: ${tab.taskId ? '#' + tab.taskId : 'None'}` });
      showTerminalMessages();
      input.value = "";
    }
    return;
  }
  const projectMatch = msg.match(/^\/project(?:\s+(.+))?/i);
  if (projectMatch) {
    if (projectMatch[1]) {
      const projectPath = projectMatch[1].trim();
      const oldSessionId = tab.localSessionId;
      tab.project = projectPath;
      tab.messages.push({ role: "info", content: `Project context set to ${projectPath}` });
      showTerminalMessages();
      input.value = "";
      if (oldSessionId) {
        tab.messages.push({ role: "info", content: `Restarting session with project context...` });
        showTerminalMessages();
        fetch(`${API}/api/agents/terminal/${oldSessionId}/stop`, {method: "POST"}).catch(() => {});
        tab.localSessionId = null;
        tab.hermesSessionId = null;
        tab.status = "new";
        startTerminalSession(tab);
      }
    } else {
      tab.messages.push({ role: "info", content: `Current Project: ${tab.project || 'None'}` });
      showTerminalMessages();
      input.value = "";
    }
    return;
  }
  const modelMatch = msg.match(/^\/model\s+(.+)/i);
  if (modelMatch) {
    const model = modelMatch[1].trim();
    const oldSessionId = tab.localSessionId;
    tab.model = model;
    tab.messages.push({ role: "info", content: `Model context set to ${model}` });
    showTerminalMessages();
    input.value = "";
    if (oldSessionId) {
      tab.messages.push({ role: "info", content: `Restarting session with model context...` });
      showTerminalMessages();
      fetch(`${API}/api/agents/terminal/${oldSessionId}/stop`, {method: "POST"}).catch(() => {});
      tab.localSessionId = null;
      tab.hermesSessionId = null;
      tab.status = "new";
      startTerminalSession(tab);
    }
    return;
  }
  const resumeMatch = msg.match(/^\/resume(?:\s+(.+))?/i);
  if (resumeMatch) {
    if (resumeMatch[1]) {
      addTerminalTabWithResume(resumeMatch[1].trim());
      input.value = "";
    } else {
      tab.messages.push({ role: "error", content: `Usage: /resume <session_id>` });
      showTerminalMessages();
      input.value = "";
    }
    return;
  }
  if (msg === "/status" || msg === "/s") {
    const p = tab.profile || "default";
    const m = tab.model || "—";
    const t = tab.taskId ? `#${tab.taskId}` : "none";
    const prj = tab.project || "—";
    const sid = tab.hermesSessionId || tab.localSessionId || "—";
    tab.messages.push({ role: "info", content: `Profile: ${p}\nModel: ${m}\nTask: ${t}\nProject: ${prj}\nSession: ${sid}` });
    showTerminalMessages();
    input.value = "";
    return;
  }
  if (msg === "/end") {
    fetch(`${API}/api/agents/terminal/${tab.localSessionId}/stop`, {method: "POST"}).catch(() => {});
    tab.localSessionId = null;
    tab.status = "ended";
    tab.messages.push({ role: "info", content: "Session ended." });
    renderTerminalTabs();
    showTerminalMessages();
    input.value = "";
    input.disabled = true;
    input.placeholder = "Session ended";
    return;
  }

  terminalSending = true;
  input.value = "";
  input.disabled = true;
  const profileLabel = tab.profile && tab.profile !== "default" ? tab.profile : "Hermes";
  tab.messages.push({ role: "user", label: "You", content: msg });
  showTerminalMessages();
  tab.messages.push({ role: "loading", content: "Thinking..." });
  showTerminalMessages();
  
  // Start elapsed timer
  loadingStartTime = Date.now();
  if (loadingTimer) clearInterval(loadingTimer);
  loadingTimer = setInterval(() => {
    const elapsed = Math.floor((Date.now() - loadingStartTime) / 1000);
    const loadingMsg = tab.messages.find(m => m.role === "loading");
    if (loadingMsg) {
      loadingMsg.content = `Thinking... ${elapsed}s`;
      showTerminalMessages();
    }
  }, 1000);
  
  try {
    const res = await fetch(`${API}/api/agents/terminal/${tab.localSessionId}/chat`, {
      method: "POST", headers: {"Content-Type": "application/json"},
      body: JSON.stringify({message: msg})
    });
    const data = await res.json();
    if (loadingTimer) { clearInterval(loadingTimer); loadingTimer = null; }
    tab.messages.pop();
    if (data.end) {
      tab.messages.push({ role: "info", content: data.response });
      tab.localSessionId = null;
      tab.status = "ended";
      renderTerminalTabs();
      showTerminalMessages();
      document.getElementById("terminalInlineInput").disabled = true;
      document.getElementById("terminalInlineInput").placeholder = "Session ended";
    } else if (data.response) {
      tab.messages.push({ role: "assistant", label: profileLabel, content: data.response });
      showTerminalMessages();
    } else {
      tab.messages.push({ role: "error", content: data.error || "No response" });
      showTerminalMessages();
    }
  } catch (e) {
    if (loadingTimer) { clearInterval(loadingTimer); loadingTimer = null; }
    tab.messages.pop();
    tab.messages.push({ role: "error", content: `Request failed: ${e.message}` });
    showTerminalMessages();
  } finally {
    terminalSending = false;
    input.disabled = false;
    input.focus();
    saveTerminalState();
  }
}

function showHelp(tab) {
  if (!tab) tab = terminalTabs[terminalActiveTab];
  if (!tab) return;
  tab.messages.push({ role: "info", content: "Available commands:\n  /status       – Show session info (profile, model, task, project)\n  /task <id>    – Set task context (#000, 00, 0)\n  /resume <id>  – Resume a session by ID\n  /project <p>  – Set project path for context\n  /model [name] – Show/switch model\n  /end          – End this session\n  /help         – Show this help" });
  showTerminalMessages();
    update2DWorld();
}

// ── Modal Terminal (legacy, single-session) ────────────────────────────

function closeTerminalModal() {
  document.getElementById("terminalModal").classList.remove("active");
}

async function openTerminalModal() {
  document.getElementById("terminalModal").classList.add("active");
  const sel = document.getElementById("terminalProfileSelect");
  try {
    const res = await fetch(`${API}/api/agents/terminal/profiles`);
    const profiles = await res.json();
    sel.innerHTML = profiles.map(p => `<option value="${p}">${p}</option>`).join("");
  } catch (e) {
    sel.innerHTML = '<option value="default">default</option>';
  }
  document.getElementById("terminalInput").value = "";
  document.getElementById("terminalInput").disabled = true;
  document.getElementById("terminalInput").placeholder = "Start a session...";
  document.getElementById("terminalBody").innerHTML =
    '<div style="padding:16px;color:var(--on-surface-variant);text-align:center;">Press <strong>New</strong> or <strong>Resume</strong> to begin.</div>';
}

async function startTerminal() {
  const profile = document.getElementById("terminalProfileSelect").value;
  document.getElementById("terminalTitle").textContent = `Terminal [${profile}]`;
  document.getElementById("terminalInput").disabled = true;
  document.getElementById("terminalBody").innerHTML = "";
  const profileLabel = profile !== "default" ? profile : "Hermes";
  termMsg("terminalBody", "info", `Starting session (profile: ${profile})...`);
  if (modalSessionId) {
    await fetch(`${API}/api/agents/terminal/${modalSessionId}/stop`, {method: "POST"}).catch(() => {});
    modalSessionId = null;
  }
  try {
    const res = await fetch(`${API}/api/agents/terminal/start`, {
      method: "POST", headers: {"Content-Type": "application/json"},
      body: JSON.stringify({profile})
    });
    const data = await res.json();
    modalSessionId = data.id;
    termMsg("terminalBody", "info", `Session ready (${data.hermes_session_id || data.id})`);
    document.getElementById("terminalInput").disabled = false;
    document.getElementById("terminalInput").placeholder = "Type a message...";
    document.getElementById("terminalInput").focus();
  } catch (e) {
    termMsg("terminalBody", "error", `Failed: ${e.message}`);
  }
}

let modalSessionId = null;

async function sendTerminalMessage() {
  const input = document.getElementById("terminalInput");
  const msg = input.value.trim();
  if (!msg || !modalSessionId || terminalSending) return;
  terminalSending = true;
  input.value = "";
  input.disabled = true;
  const profile = document.getElementById("terminalProfileSelect").value;
  const profileLabel = profile !== "default" ? profile : "Hermes";
  termMsg("terminalBody", "user", msg);
  termMsg("terminalBody", "info", "Waiting...");
  try {
    const res = await fetch(`${API}/api/agents/terminal/${modalSessionId}/chat`, {
      method: "POST", headers: {"Content-Type": "application/json"},
      body: JSON.stringify({message: msg})
    });
    const data = await res.json();
    document.getElementById("terminalBody").lastElementChild.remove();
    if (data.response) {
      termMsg("terminalBody", "assistant", data.response, profileLabel);
    } else {
      termMsg("terminalBody", "error", data.error || "No response");
    }
  } catch (e) {
    document.getElementById("terminalBody").lastElementChild.remove();
    termMsg("terminalBody", "error", `Request failed: ${e.message}`);
  } finally {
    terminalSending = false;
    input.disabled = false;
    input.focus();
  }
}

async function resumeSession(sessionId) {
  const panel = document.getElementById("terminalPanelBody");
  if (panel) {
    addTerminalTabWithResume(sessionId);
    return;
  }
  await openTerminalModal();
  const profile = document.getElementById("terminalProfileSelect").value;
  document.getElementById("terminalTitle").textContent = `Resuming ${sessionId}`;
  document.getElementById("terminalBody").innerHTML = "";
  termMsg("terminalBody", "info", `Loading session ${sessionId} history...`);
  if (modalSessionId) {
    await fetch(`${API}/api/agents/terminal/${modalSessionId}/stop`, {method: "POST"}).catch(() => {});
    modalSessionId = null;
  }
  try {
    let history = [];
    try {
      const h = await fetch(`${API}/api/agents/sessions/${encodeURIComponent(sessionId)}/messages`);
      if (h.ok) {
        const hd = await h.json();
        history = (hd.messages || []).map(m => ({ role: m.role || "assistant", content: m.content || "" }));
        const userMsgs = history.filter(m => m.role === "user").length;
        const asstMsgs = history.filter(m => m.role === "assistant").length;
        for (const m of history) {
          termMsg("terminalBody", m.role, m.content);
        }
        if (history.length > 0) {
          termMsg("terminalBody", "info", `── History end (${history.length} messages · ${userMsgs} user · ${asstMsgs} assistant) ──`);
        }
      }
    } catch (e) {
      termMsg("terminalBody", "info", `History fetch error: ${e.message}`);
    }

    const res = await fetch(`${API}/api/agents/terminal/start`, {
      method: "POST", headers: {"Content-Type": "application/json"},
      body: JSON.stringify({profile, session_id: sessionId, history})
    });
    const data = await res.json();
    modalSessionId = data.id;
    const modelInfo = data.model ? ` · ${data.model}` : "";
    termMsg("terminalBody", "info", `Resumed ${data.hermes_session_id || data.id}${modelInfo}`);
    document.getElementById("terminalInput").disabled = false;
    document.getElementById("terminalInput").placeholder = "Continue...";
    document.getElementById("terminalInput").focus();
  } catch (e) {
    termMsg("terminalBody", "error", `Failed: ${e.message}`);
  }
}

async function addTerminalTabWithResume(sessionId, passedProfile = null) {
  const profile = passedProfile || document.getElementById("terminalProfileSelectInline").value || "default";
  tabCounter++;
  const tab = { tabNum: tabCounter, localSessionId: null, hermesSessionId: sessionId,
    profile, model: null, messages: [], status: "new", taskId: null };
  terminalTabs.push(tab);
  terminalActiveTab = terminalTabs.length - 1;
  renderTerminalTabs();
  showTerminalMessages();
  tab.messages.push({ role: "info", content: `Resuming session ${sessionId} (${profile})...` });
  showTerminalMessages();
  try {
    let history = [];
    let historySource = "";
    try {
      const h = await fetch(`${API}/api/agents/sessions/${encodeURIComponent(sessionId)}/messages`);
      if (h.ok) {
        const hd = await h.json();
        history = (hd.messages || []).map(m => ({ role: m.role || "assistant", content: m.content || "" }));
        historySource = "gateway";
      } else {
        tab.messages.push({ role: "info", content: `History fetch returned ${h.status}` });
        showTerminalMessages();
      }
    } catch (e) {
      tab.messages.push({ role: "info", content: `History fetch error: ${e.message}` });
      showTerminalMessages();
    }

    const res = await fetch(`${API}/api/agents/terminal/start`, {
      method: "POST", headers: {"Content-Type": "application/json"},
      body: JSON.stringify({profile, session_id: sessionId, history})
    });
    const data = await res.json();
    tab.localSessionId = data.id;
    tab.hermesSessionId = data.hermes_session_id || sessionId;
    tab.model = data.model;
    tab.status = "connected";
    const restoredHistory = (data.history && data.history.length ? data.history : history);
    const profileLabel = profile !== "default" ? profile : "Hermes";
    tab.messages = restoredHistory.map((m, i) => ({
      role: m.role,
      content: m.content,
      label: m.role === "assistant" ? (m.label || profileLabel) : (m.role === "user" ? "You" : undefined),
      ts: m.ts || Date.now() - (restoredHistory.length - i) * 1000
    }));
    const modelInfo = data.model ? ` · ${data.model}` : "";
    const userMsgs = tab.messages.filter(m => m.role === "user").length;
    const asstMsgs = tab.messages.filter(m => m.role === "assistant").length;
    let ctxSummary = "";
    if (userMsgs || asstMsgs) {
      ctxSummary = ` · ${userMsgs} user · ${asstMsgs} assistant`;
    }
    if (tab.messages.length > 0) {
      tab.messages.push({ role: "info", content: `── History loaded (${tab.messages.length} messages${ctxSummary}) ──` });
    }
    tab.messages.push({ role: "info", content: `Resumed ${tab.hermesSessionId}${modelInfo}` });
    renderTerminalTabs();
    showTerminalMessages();
    document.getElementById("terminalInlineInput").focus();
  } catch (e) {
    tab.messages.push({ role: "error", content: `Failed: ${e.message}` });
    tab.status = "error";
    showTerminalMessages();
  }
}

// ── End / Delete (CLI Sessions tab) ──────────────────────────────────

async function endSession(sessionId) {
  if (!confirm(`End session ${sessionId}?`)) return;
  try {
    await fetch(`${API}/api/agents/terminal/session/${encodeURIComponent(sessionId)}/end`, {method: "POST"});
    await fetch(`${API}/api/agents/sessions/${encodeURIComponent(sessionId)}`, {method: "DELETE"});
    refreshHermesSessions();
  } catch (e) {
    alert(`Failed: ${e.message}`);
  }
}

async function deleteSession(sessionId) {
  if (!confirm(`Delete session ${sessionId}?`)) return;
  try {
    await fetch(`${API}/api/agents/sessions/${encodeURIComponent(sessionId)}`, {method: "DELETE"});
    refreshHermesSessions();
  } catch (e) {
    alert(`Failed: ${e.message}`);
  }
}

// ── Init ──────────────────────────────────────────────────────────────
// Drag-to-scroll tabs
function initTabScroll() {
  const el = document.getElementById("terminalTabBar");
  if (!el) return;
  let isDown = false, startX, scrollLeft;
  el.addEventListener("mousedown", e => { isDown = true; startX = e.pageX - el.offsetLeft; scrollLeft = el.scrollLeft; });
  el.addEventListener("mouseleave", () => { isDown = false; });
  el.addEventListener("mouseup", () => { isDown = false; });
  el.addEventListener("mousemove", e => { if (!isDown) return; e.preventDefault(); el.scrollLeft = scrollLeft - (e.pageX - el.offsetLeft - startX); });
}

// Save terminal state before page unload
window.addEventListener("beforeunload", saveTerminalState);

async function restoreStaleSession(tab, idx) {
  if (!tab.hermesSessionId) return;
  const found = terminalTabs.indexOf(tab);
  if (found < 0) return;
  await addTerminalTabWithResume(tab.hermesSessionId);
  const restoredIdx = terminalTabs.length - 1;
  if (found !== restoredIdx) {
    await closeTerminalTab(found);
    if (terminalActiveTab >= restoredIdx - 1) {
      terminalActiveTab = restoredIdx - 1;
      renderTerminalTabs();
    }
  }
}

function initTerminal() {
  if (restoreTerminalState()) {
    renderTerminalTabs();
    showTerminalMessages();
    if (terminalTabs.length > 0) {
      if (terminalTabs.some(t => t.status === "stale" && t.messages.length > 0)) {
        const active = terminalTabs[terminalActiveTab];
        if (active && active.status === "stale") {
          const last = active.messages[active.messages.length - 1];
          if (!last || last.content !== "── Page reloaded ──") {
            active.messages.push({ role: "info", content: "── Page reloaded ──" });
          }
        }
      }
      showTerminalMessages();
      const body = document.getElementById("terminalMessages");
      if (body) {
        const btn = document.createElement("div");
        btn.style.cssText = "padding:8px;text-align:center;display:flex;gap:6px;justify-content:center;flex-wrap:wrap;";
        const staleWithId = terminalTabs.filter(t => t.status === "stale" && t.hermesSessionId);
        if (staleWithId.length > 0) {
          const info = document.createElement("div");
          info.style.cssText = "font-size:11px;color:var(--on-surface-variant);margin-bottom:4px;width:100%;";
          info.textContent = `${staleWithId.length} session(s) can be restored`;
          btn.appendChild(info);
          const restoreAllBtn = document.createElement("button");
          restoreAllBtn.className = "btn";
          restoreAllBtn.style.cssText = "font-size:11px;";
          restoreAllBtn.innerHTML = `<i class="ph ph-arrow-clockwise" style="font-size:10px;"></i> Restore all (${staleWithId.length})`;
          restoreAllBtn.onclick = async () => {
            restoreAllBtn.disabled = true;
            restoreAllBtn.textContent = "Restoring...";
            for (let i = 0; i < staleWithId.length; i++) {
              const idx = terminalTabs.indexOf(staleWithId[i]);
              if (idx >= 0) await restoreStaleSession(staleWithId[i], idx);
            }
          };
          btn.appendChild(restoreAllBtn);
        }
        const reconnectBtn = document.createElement("button");
        reconnectBtn.className = "btn";
        reconnectBtn.style.cssText = "font-size:11px;";
        reconnectBtn.textContent = "Reconnect active tab";
        reconnectBtn.onclick = () => reconnectTerminalTab(terminalActiveTab);
        btn.appendChild(reconnectBtn);
        body.appendChild(btn);
      }
    }
  } else {
    const body = document.getElementById("terminalMessages");
    if (body) body.innerHTML =
      '<div style="padding:16px;color:var(--on-surface-variant);text-align:center;">Press <strong>+ New</strong> to start a terminal session.</div>';
  }
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", () => { initTabScroll(); initTerminal(); loadAgents(); _hookTypingDetection(); });
} else {
  initTabScroll();
  initTerminal();
  loadAgents();
  _hookTypingDetection();
}
setInterval(loadAgents, 60000);


function openTerminalSessionsModal() {
    const modal = document.getElementById("terminalSessionsModal");
    if (modal) {
        modal.classList.add("active");
        modal.style.display = "";
        refreshTerminalSessions();
    }
}

function closeTerminalSessionsModal() {
    const modal = document.getElementById("terminalSessionsModal");
    if (modal) modal.classList.remove("active");
}

async function refreshTerminalSessions() {
    // Used by both agentConfigModal (Sessions tab) and agentPanelModal (Sessions view)
    const container = document.getElementById("terminalSessionsList") || document.getElementById("hermesSessionsList");
    if (!container) return;
    container.innerHTML = '<div style="padding:20px;text-align:center;"><i class="ph ph-spinner" style="animation:spin 1s linear infinite;"></i> Loading...</div>';
    try {
        const res = await fetch(`${API}/api/agents/sessions`);
        const data = await res.json();

        const countEl = document.getElementById("sessionsCount");
        const gatewayEl = document.getElementById("sessionsGateway");

        if (!data.sessions || data.sessions.length === 0) {
            if (countEl) countEl.textContent = "";
            container.innerHTML = '<div style="padding:20px;text-align:center;">No sessions found</div>';
            return;
        }

        if (countEl) countEl.textContent = `(${data.sessions.length})`;
        if (gatewayEl) {
            gatewayEl.textContent = data.gateway || (data.fallback ? "cached" : "");
        }

        // Build task ID lookup from active tabs
        const tabTaskMap = {};
        terminalTabs.forEach(t => {
            if (t.hermesSessionId && t.taskId) tabTaskMap[t.hermesSessionId] = t.taskId;
        });

        // Check if we're in the agent panel sessions view (has search input)
        const isPanelView = !!document.getElementById('sessionsSearchInput');

        let html = '';
        if (isPanelView) {
            // Panel view: checkbox, search handled by filterSessions()
            html = `
            <div style="display:flex;align-items:center;gap:8px;padding: 8px 0px 8px;border-bottom:1px solid var(--border-color);position:sticky;top: -8px;background:var(--header-bg);z-index:2;">
                <input type="checkbox" id="sessSelectAll" title="Select all" onchange="toggleSelectAllSessions(this.checked)" style="cursor:pointer;width:14px;height:14px;">
                <span style="font-size:11px;color:var(--on-surface-variant);flex:1;">Session</span>
                <span style="font-size:11px;color:var(--on-surface-variant);width:80px;">Profile</span>
                <span style="font-size:11px;color:var(--on-surface-variant);width:100px;">Last Active</span>
                <span style="width:80px;text-align:right;">
                    <button class="agent-sync-btn" id="sessDeleteSelectedBtn" onclick="deleteSelectedSessions()" style="font-size:10px;padding:2px 7px;color:#f85149;border-color:#f85149;display:none;">
                        <i class="ph ph-trash" style="font-size:10px;"></i> Delete
                    </button>
                </span>
            </div>`;
        }

        data.sessions.forEach(s => {
            // Update tab title
            const tab = terminalTabs.find(t => t.hermesSessionId === s.id);
            if (tab && s.title && s.title !== s.id) {
                tab.title = s.title;
                renderTerminalTabs();
            }

            // Detect task badge — from tab map or from session title
            let taskBadge = '';
            const taskId = tabTaskMap[s.id] ||
                (s.title && s.title.match(/talaria-task-(\d+)/)?.[1]) ||
                (s.title && s.title.match(/check-#(\d+)/)?.[1]);
            if (taskId) {
                taskBadge = `<span style="font-size:9px;padding:1px 5px;border-radius:3px;background:var(--primary);color:#fff;font-weight:700;margin-left:4px;">#${escHtml(String(taskId))}</span>`;
            }

            const isCheck = s.title && s.title.startsWith('check-');
            const rowBg = isCheck ? 'rgba(100,180,255,0.04)' : 'transparent';

            html += `
            <div class="sess-row" data-sid="${escHtml(s.id)}" style="display:flex;align-items:center;gap:8px;padding:8px 0;border-bottom:1px solid var(--border-color);border-radius:4px;background:${rowBg};transition:background 0.15s;"
                onmouseover="this.style.background='var(--surface-hover)'"
                onmouseout="this.style.background='${rowBg}'">
                <input type="checkbox" class="sess-checkbox" data-sid="${escHtml(s.id)}" onchange="onSessionCheckChange()" style="cursor:pointer;width:14px;height:14px;flex-shrink:0;">
                <div style="flex:1;overflow:hidden;display:flex;flex-direction:column;gap:2px;min-width:0;">
                    <div style="display:flex;align-items:center;gap:4px;flex-wrap:wrap;">
                        <strong style="font-size:11px;color:var(--primary-color);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:180px;">${escHtml(s.id)}</strong>
                        ${taskBadge}
                    </div>
                    <span style="font-size:11px;color:var(--on-surface-variant);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">${escHtml(s.title || 'Untitled')}</span>
                </div>
                <div style="width:80px;flex-shrink:0;">
                    <span class="badge" style="background:var(--surface-variant);color:var(--text-color);padding:3px 7px;border-radius:10px;font-size:10px;font-weight:500;">${escHtml(s.profile || 'default')}</span>
                </div>
                <div style="width:100px;font-size:11px;color:var(--on-surface-variant);flex-shrink:0;">${escHtml(s.last_active_fmt || '')}</div>
                <div style="width:80px;display:flex;gap:4px;justify-content:flex-end;flex-shrink:0;">
                    <button class="icon-btn" style="color:var(--primary-color);" title="Resume" onclick="resumeSessionInTab('${escHtml(s.id)}', '${escHtml(s.profile || 'default')}')">
                        <i class="ph ph-play-circle" style="font-size:16px;"></i>
                    </button>
                    <button class="icon-btn" style="color:#f85149;" title="Delete" onclick="deleteTerminalSession('${escHtml(s.id)}')">
                        <i class="ph ph-trash" style="font-size:16px;"></i>
                    </button>
                </div>
            </div>`;
        });

        container.innerHTML = html;
    } catch (e) {
        container.innerHTML = `<div style="padding:20px;color:#f85149;">Error: ${e.message}</div>`;
    }
}

function onSessionCheckChange() {
    const checked = document.querySelectorAll('.sess-checkbox:checked');
    const all = document.querySelectorAll('.sess-checkbox');
    const selectAll = document.getElementById('sessSelectAll');
    const deleteBtn = document.getElementById('sessDeleteSelectedBtn');
    if (selectAll) selectAll.checked = checked.length === all.length && all.length > 0;
    if (deleteBtn) deleteBtn.style.display = checked.length > 0 ? 'inline-flex' : 'none';
}

function toggleSelectAllSessions(checked) {
    document.querySelectorAll('.sess-checkbox').forEach(cb => cb.checked = checked);
    onSessionCheckChange();
}

async function deleteSelectedSessions() {
    const checked = [...document.querySelectorAll('.sess-checkbox:checked')];
    if (!checked.length) return;
    if (!confirm(`Delete ${checked.length} session(s)?`)) return;
    const ids = checked.map(cb => cb.dataset.sid);
    const succeeded = [];
    const failed = [];
    const total = ids.length;
    // Disable the button + show progress in its label
    const btn = document.getElementById('sessDeleteSelectedBtn');
    const restoreBtn = () => { if (btn) { btn.disabled = false; btn.innerHTML = '<i class="ph ph-trash" style="font-size:10px;"></i> Delete'; } };
    if (btn) { btn.disabled = true; btn.textContent = `Deleting 0/${total}…`; }
    let done = 0;
    for (const id of ids) {
        try {
            const res = await fetch(`${API}/api/agents/sessions/${encodeURIComponent(id)}`, { method: 'DELETE' });
            if (res.ok) {
                succeeded.push(id);
            } else {
                let detail = '';
                try { detail = (await res.json()).error || ''; } catch (_) {}
                failed.push({ id, status: res.status, detail });
            }
        } catch (e) {
            failed.push({ id, status: 0, detail: e.message });
        }
        done += 1;
        if (btn) btn.textContent = `Deleting ${done}/${total}…`;
    }
    refreshTerminalSessions();
    restoreBtn();
    if (failed.length) {
        const failedIds = failed.map(f => f.id).join(', ');
        alert(`Deleted ${succeeded.length}/${total}. Failed: ${failedIds}`);
    } else if (total > 0) {
        alert(`Deleted ${total} session${total === 1 ? '' : 's'}.`);
    }
}

async function deleteTerminalSession(sessionId) {
    if (!confirm(`Delete session ${sessionId}?`)) return;
    try {
        const res = await fetch(`${API}/api/agents/sessions/${encodeURIComponent(sessionId)}`, { method: "DELETE" });
        if (res.status === 404) {
            alert('Session already gone — refreshing list.');
            refreshTerminalSessions();
            return;
        }
        if (!res.ok) {
            let detail = '';
            try { detail = (await res.json()).error || ''; } catch (_) {}
            throw new Error(detail || `Failed to delete session (${res.status})`);
        }
        refreshTerminalSessions();
        alert(`Deleted session ${sessionId}.`);
    } catch (e) {
        alert(e.message);
    }
}

function resumeSessionInTab(sid, profile="default") {
    closeTerminalSessionsModal();
    const existingIdx = terminalTabs.findIndex(t => t.hermesSessionId === sid);
    if (existingIdx !== -1) {
        switchTerminalTab(existingIdx);
    } else {
        addTerminalTabWithResume(sid, profile);
    }
}


function openAgentPanelModal() {
    const modal = document.getElementById("agentPanelModal");
    if (modal) modal.classList.add("active");
    renderTerminalTabs();
    update2DWorld();
    // Load saved terminal config and populate model selector
    _loadTerminalModelConfig();

    // Restore last active view
    const savedView = localStorage.getItem('talaria_agent_view') || 'terminal';
    if (savedView !== 'terminal') {
        setTimeout(() => switchAgentView(savedView), 50);
    }

    // Initialize sprite previews if office preview was open
    if (localStorage.getItem('talaria_office_preview') === 'true') {
        setTimeout(() => toggleOfficePreview(), 100);
    }
}

function closeAgentPanelModal() {
    const modal = document.getElementById("agentPanelModal");
    if (modal) modal.classList.remove("active");
}

// ── Agent Panel View Switching ───────────────────────────────────────────────
let _agentActiveView = 'terminal'; // 'terminal' | 'sessions'
let _officePreviewOpen = false;

function switchAgentView(view) {
    _agentActiveView = view;

    // Update tab buttons
    document.querySelectorAll('.agent-nav-tab').forEach(btn => {
        const isActive = btn.dataset.view === view;
        btn.classList.toggle('active', isActive);
        btn.style.color = isActive ? 'var(--primary-color)' : 'var(--on-surface-variant)';
        btn.style.borderBottomColor = isActive ? 'var(--primary-color)' : 'transparent';
    });

    // Update view visibility
    const terminalView = document.getElementById('agentTerminalView');
    const sessionsView = document.getElementById('agentSessionsView');

    if (view === 'terminal') {
        terminalView.style.display = 'flex';
        sessionsView.style.display = 'none';
        renderTerminalTabs();
        showTerminalMessages();
    } else {
        terminalView.style.display = 'none';
        sessionsView.style.display = 'flex';
        refreshTerminalSessions();
    }

    // Save preference
    localStorage.setItem('talaria_agent_view', view);
}

function toggleOfficePreview() {
    _officePreviewOpen = !_officePreviewOpen;
    const world = document.getElementById('agent2DWorld');
    const btn = document.getElementById('toggleOfficePreviewBtn');

    if (_officePreviewOpen) {
        if (world) world.style.display = 'block';
        btn.style.color = 'var(--primary-color)';
        localStorage.setItem('talaria_office_preview', 'true');
    } else {
        if (world) world.style.display = 'none';
        btn.style.color = '';
        localStorage.setItem('talaria_office_preview', 'false');
    }
}

function renderSpritePreviews() {
    const container = document.getElementById('spritePreviewContainer');
    if (!container) return;

    container.innerHTML = AGENT_SPRITES.map(sprite => {
        const color = getColorForString(sprite);
        return `
            <div style="display:flex;flex-direction:column;align-items:center;gap:4px;padding:8px;background:var(--surface);border:1px solid var(--border-color);border-radius:6px;min-width:80px;">
                <div style="width:64px;height:64px;background:url('assets/${sprite}.png') 0px 0px no-repeat;background-size:512px 512px;image-rendering:pixelated;border:1px solid ${color};border-radius:4px;"></div>
                <span style="font-size:10px;font-weight:600;color:${color};">${sprite}</span>
                <span style="font-size:9px;color:var(--on-surface-variant);">128×128px</span>
            </div>
        `;
    }).join('');
}

// ── Terminal model/provider settings ─────────────────────────────────────────

async function _loadTerminalModelConfig() {
    try {
        const res = await fetch(`${API}/api/agents/terminal/config`);
        const cfg = await res.json();
        const providerInput = document.getElementById('terminalProviderUrl');
        const defaultModelInput = document.getElementById('terminalDefaultModel');
        if (providerInput) providerInput.value = cfg.provider_url || 'http://127.0.0.1:20821';
        if (defaultModelInput) defaultModelInput.value = cfg.model || '';
        // Populate model dropdown
        await fetchTerminalModels(cfg.provider_url);
        // Set selected model
        const sel = document.getElementById('terminalModelInline');
        if (sel && cfg.model) {
            // Add saved model as option if not in list
            if (![...sel.options].some(o => o.value === cfg.model)) {
                const opt = document.createElement('option');
                opt.value = cfg.model;
                opt.textContent = cfg.model;
                sel.insertBefore(opt, sel.firstChild);
            }
            sel.value = cfg.model;
        }
    } catch (e) { /* ignore */ }
}

async function loadTerminalConfig() {
    const urlInput = document.getElementById('terminalProviderUrl');
    const apiKeyInput = document.getElementById('terminalApiKey');
    const defaultModelInput = document.getElementById('terminalDefaultModel');
    const backendSelect = document.getElementById('terminalBackend');
    try {
        // 1. Load saved terminal config
        const res = await fetch(`${API}/api/agents/terminal/config`);
        const cfg = res.ok ? await res.json() : {};
        let providerUrl = cfg.provider_url || '';
        let apiKey = cfg.api_key || '';
        let savedModel = cfg.model || '';
        let backend = cfg.backend || 'hermes-agent';

        // 2. If no saved provider_url, pull from Hermes agent config
        if (!providerUrl) {
            try {
                const hermesRes = await fetch(`${API}/api/agents/hermes-local-config`);
                if (hermesRes.ok) {
                    const hc = await hermesRes.json();
                    if (hc.base_url) providerUrl = hc.base_url;
                    if (hc.api_key) apiKey = apiKey || hc.api_key;
                }
            } catch (e) { /* ignore */ }
        }

        // 3. Apply to UI
        if (providerUrl && urlInput) {
            urlInput.value = providerUrl;
            urlInput.placeholder = '';
        }
        if (apiKey && apiKeyInput) {
            apiKeyInput.value = apiKey;
        }
        if (savedModel && defaultModelInput) {
            defaultModelInput.value = savedModel;
        }
        if (backendSelect) {
            backendSelect.value = backend;
        }
    } catch (e) { /* ignore */ }
}

function openTerminalModelSettings() {
    const panel = document.getElementById('terminalModelSettingsPanel');
    if (!panel) return;
    const isOpen = panel.style.display !== 'none';
    panel.style.display = isOpen ? 'none' : 'flex';
    if (!isOpen) {
        loadTerminalConfig().then(() => fetchTerminalModels());
    }
}

async function fetchTerminalModels(providerUrl) {
    const sel = document.getElementById('terminalModelInline');
    if (!sel) return;
    const urlInput = document.getElementById('terminalProviderUrl');
    const url = providerUrl || (urlInput && urlInput.value.trim());
    if (!url) {
        sel.innerHTML = '<option value="">set provider URL first</option>';
        return;
    }
    sel.innerHTML = '<option value="">fetching...</option>';
    try {
        const apiKeyInput = document.getElementById('terminalApiKey');
        const apiKey = apiKeyInput ? apiKeyInput.value.trim() : '';
        const headers = { 'Accept': 'application/json' };
        if (apiKey) headers['Authorization'] = `Bearer ${apiKey}`;
        const res = await fetch(`${API}/api/agents/terminal/models?provider_url=${encodeURIComponent(url)}`, { headers });
        const data = await res.json();
        if (data.models && data.models.length) {
            sel.innerHTML = data.models.map(m =>
                `<option value="${escHtml(m)}">${escHtml(m)}</option>`
            ).join('');
            // Update provider URL field if server found a different one
            if (data.provider_url && urlInput) urlInput.value = data.provider_url;
        } else {
            sel.innerHTML = '<option value="">no models found</option>';
        }
    } catch (e) {
        sel.innerHTML = '<option value="">fetch failed</option>';
    }
}

async function saveTerminalModelConfig() {
    const providerUrl = document.getElementById('terminalProviderUrl')?.value.trim() || '';
    const apiKey = document.getElementById('terminalApiKey')?.value.trim() || '';
    const model = document.getElementById('terminalModelInline')?.value ||
                  document.getElementById('terminalDefaultModel')?.value.trim() || '';
    const backend = document.getElementById('terminalBackend')?.value || 'hermes-agent';
    try {
        await fetch(`${API}/api/agents/terminal/config`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ provider_url: providerUrl, api_key: apiKey, model, backend })
        });
        showToast(`Saved: ${backend} / ${model || 'no model'}`, 'success');
        // Update the hidden input to reflect saved model
        const hidden = document.getElementById('terminalDefaultModel');
        if (hidden) hidden.value = model;
        document.getElementById('terminalModelSettingsPanel').style.display = 'none';
    } catch (e) {
        showToast('Save failed', 'error');
    }
}


// Each sheet is 128x128, 8x8 grid of 16x16 frames
// Row 0 = idle (front)
// Row 1 = working (front, legacy)
// Row 2 = walk right
// Row 3 = walk left
// Row 4 = sitting at desk (back view, typing)
// Row 5 = sitting idle (back view)
const AGENT_SPRITES = ['office_man', 'office_woman', 'alien', 'hacker', 'robot'];
const SPRITE_FRAME = 16;   // px per frame in the sheet
const SPRITE_SCALE = 4;    // display scale (16*4 = 64px rendered)
const SPRITE_COLS  = 8;
const SPRITE_FPS   = 6;    // frames per second for walk cycle

// Track animation state per avatar
let _spriteAnimFrame = {};
let _spriteAnimTimer = null;

// ── Profile-based avatar system ──────────────────────────────────
// Each profile gets a persistent avatar with state machine:
//   entering → idle ↔ working (when agent thinking)
//   user typing → walking back and forth
let _avatarState = {};  // keyed by profile name
// { profile: { sprite, state, x, targetX, direction, element } }
// states: 'entering', 'idle', 'working', 'walking', 'typing'

const AVATAR_SPEED = 3.0;   // px per animation tick when walking
const AVATAR_IDLE_RANGE = 40; // px wander range when typing
let _avatarWorldWidth = 0;
let _profileSpriteMap = {};  // persist profile→sprite assignment
let _typingTimer = null;

function _initProfileSprites() {
    // Load saved mapping
    try {
        const saved = localStorage.getItem('talaria_profile_sprites');
        if (saved) _profileSpriteMap = JSON.parse(saved);
    } catch(e) {}
}
_initProfileSprites();

function _assignSprite(profile) {
    if (_profileSpriteMap[profile]) return _profileSpriteMap[profile];
    // Assign next unused sprite, or cycle
    const used = new Set(Object.values(_profileSpriteMap));
    let sprite = AGENT_SPRITES.find(s => !used.has(s));
    if (!sprite) {
        // All used, hash profile name to pick
        let hash = 0;
        for (let i = 0; i < profile.length; i++) hash = ((hash << 5) - hash + profile.charCodeAt(i)) | 0;
        sprite = AGENT_SPRITES[Math.abs(hash) % AGENT_SPRITES.length];
    }
    _profileSpriteMap[profile] = sprite;
    try { localStorage.setItem('talaria_profile_sprites', JSON.stringify(_profileSpriteMap)); } catch(e) {}
    return sprite;
}

function _startSpriteAnim() {
    if (_spriteAnimTimer) return;
    _spriteAnimTimer = setInterval(() => {
        const world = document.getElementById("agent2DWorld");
        if (!world) return;
        _avatarWorldWidth = world.offsetWidth;

        Object.keys(_avatarState).forEach(profile => {
            const av = _avatarState[profile];
            if (!av || !av.element || !av.element.parentNode) return;

            // Advance animation frame
            const key = profile;
            _spriteAnimFrame[key] = ((_spriteAnimFrame[key] || 0) + 1) % SPRITE_COLS;

            // Movement logic per state
            if (av.state === 'wandering') {
                const dx = av.wanderTarget - av.x;
                if (Math.abs(dx) > 2) {
                    av.x += (dx > 0 ? AVATAR_SPEED : -AVATAR_SPEED);
                    av.direction = dx > 0 ? 'right' : 'left';
                } else {
                    // Reached wander target — pause briefly then pick new target
                    av.x = av.wanderTarget;
                    av.state = 'wander_pause';
                    av.wanderPauseTicks = Math.floor(SPRITE_FPS * (1 + Math.random() * 2));
                }
            } else if (av.state === 'wander_pause') {
                av.wanderPauseTicks--;
                if (av.wanderPauseTicks <= 0) {
                    _pickWanderTarget(av);
                    av.state = 'wandering';
                }
            } else if (av.state === 'walking_to_desk') {
                const dx = av.targetX - av.x;
                if (Math.abs(dx) > 1.5) {
                    av.x += (dx > 0 ? AVATAR_SPEED : -AVATAR_SPEED);
                    av.direction = dx > 0 ? 'right' : 'left';
                } else {
                    // Arrived at desk — sit down
                    av.x = av.targetX;
                    av.state = 'sitting';
                }
            } else if (av.state === 'sitting') {
                // Stays sitting until work completes (handled in state transitions)
            } else if (av.state === 'walking') {
                const dx = av.targetX - av.x;
                if (Math.abs(dx) > 2) {
                    av.x += (dx > 0 ? AVATAR_SPEED : -AVATAR_SPEED);
                    av.direction = dx > 0 ? 'right' : 'left';
                } else {
                    av.x = av.targetX;
                    av.state = 'idle';
                }
            }
            // 'idle' doesn't move

            // Update sprite row based on state
            let spriteRow;
            if (av.state === 'sitting') {
                spriteRow = 4;  // sitting at desk, typing (always work-driven)
            } else if (av.state === 'wandering' || av.state === 'walking' || av.state === 'walking_to_desk') {
                spriteRow = av.direction === 'right' ? 2 : 3;
            } else {
                spriteRow = 0; // idle (front-facing)
            }

            // Update DOM
            av.element.style.left = av.x + 'px';

            const col = _spriteAnimFrame[key];
            const ox = -(col * SPRITE_FRAME * SPRITE_SCALE);
            const oy = -(spriteRow * SPRITE_FRAME * SPRITE_SCALE);
            const spriteEl = av.element.querySelector(".sprite-frame");
            if (spriteEl) spriteEl.style.backgroundPosition = `${ox}px ${oy}px`;

            // Update tag
            const tag = av.element.querySelector(".tag");
            if (tag) {
                const stateLabel = av.state === 'sitting' ? 'thinking' :
                                   av.state === 'walking_to_desk' ? 'thinking' :
                                   av.tabCount > 0 ? 'connected' : 'idle';
                tag.textContent = `${profile} (${stateLabel})`;
            }
        });
    }, 1000 / SPRITE_FPS);
}

function _stopSpriteAnim() {
    if (_spriteAnimTimer) { clearInterval(_spriteAnimTimer); _spriteAnimTimer = null; }
    _spriteAnimFrame = {};
}

function _createAvatarElement(profile, spriteName) {
    const avatar = document.createElement("div");
    avatar.className = "agent-avatar";
    avatar.dataset.sprite = spriteName;
    avatar.dataset.profile = profile;

    const dispSize = SPRITE_FRAME * SPRITE_SCALE;
    const sheetSize = 128 * SPRITE_SCALE;

    avatar.innerHTML = `
        <div class="tag">${profile}</div>
        <div class="sprite-frame" style="
            width:${dispSize}px;
            height:${dispSize}px;
            background:url('assets/${spriteName}.png') 0px 0px no-repeat;
            background-size:${sheetSize}px ${sheetSize}px;
            image-rendering:pixelated;
        "></div>
    `;
    return avatar;
}

// All known profiles (fetched from API, always shown even without tabs)
let _knownProfiles = [];

function _spawnProfileAvatars(profiles) {
    _knownProfiles = profiles;
    update2DWorld();
}

// Detect which profiles have active terminals
function _getActiveProfiles() {
    const profiles = new Set();
    const profileTabs = {};
    terminalTabs.forEach(tab => {
        if (!tab.localSessionId && tab.status !== 'connected' && tab.status !== 'new') return;
        const p = tab.profile || 'default';
        profiles.add(p);
        if (!profileTabs[p]) profileTabs[p] = [];
        profileTabs[p].push(tab);
    });
    return { profiles: [...profiles], profileTabs };
}

// Check if any tab for a profile is in "loading" state (agent thinking)
function _isProfileWorking(tabs) {
    if (!tabs) return false;
    return tabs.some(tab =>
        tab.messages.length > 0 && tab.messages[tab.messages.length - 1].role === "loading"
    );
}

function update2DWorld() {
    const world = document.getElementById("agent2DWorld");
    if (!world) return;
    _avatarWorldWidth = world.offsetWidth;

    const { profiles, profileTabs } = _getActiveProfiles();

    // Merge known profiles (from API) with active tab profiles
    const allProfiles = [...new Set([..._knownProfiles, ...profiles])];

    // Calculate target positions (centered, capped width so they stay clustered)
    const avatarW = 64;
    const minGap = avatarW + 20;
    const maxTotalWidth = Math.min(_avatarWorldWidth * 0.5, 400);
    const spacing = allProfiles.length <= 1 ? 0 : Math.max(minGap, maxTotalWidth / (allProfiles.length - 1));
    const totalWidth = (allProfiles.length - 1) * spacing;
    const startX = (_avatarWorldWidth - avatarW) / 2 - totalWidth / 2;

    allProfiles.forEach((profile, index) => {
        const targetX = startX + index * spacing;
        const sprite = _assignSprite(profile);

        if (!_avatarState[profile]) {
            const el = _createAvatarElement(profile, sprite);
            el.style.left = targetX + 'px';
            world.appendChild(el);
            const av = {
                sprite, state: 'wandering', x: targetX, targetX,
                direction: 'right', element: el, tabCount: 0,
                wanderTarget: targetX, wanderPauseTicks: 0
            };
            _pickWanderTarget(av);
            _avatarState[profile] = av;
        }

        const av = _avatarState[profile];
        av.tabCount = (profileTabs[profile] || []).length;
        const wasWorking = av.state === 'sitting' || av.state === 'walking_to_desk';
        const isWorking = _isProfileWorking(profileTabs[profile]);

        // State transitions — sitting is ONLY triggered by hermes thinking (working state)
        if (isWorking && !wasWorking) {
            // Walk to nearest desk and sit down
            const desk = _nearestDesk(av.x);
            if (desk != null) {
                av.targetX = desk;
                av.state = 'walking_to_desk';
            }
        } else if (!isWorking && wasWorking) {
            // Work done — get up and resume wandering
            _pickWanderTarget(av);
            av.state = 'wandering';
        }
        // wandering/wander_pause/idle/walking left alone

        // Reattach element if removed
        if (!av.element.parentNode) {
            world.appendChild(av.element);
        }
    });

    // Remove avatars for profiles no longer active
    Object.keys(_avatarState).forEach(profile => {
        if (!allProfiles.includes(profile)) {
            const av = _avatarState[profile];
            if (av.element && av.element.parentNode) {
                av.element.remove();
            }
            delete _avatarState[profile];
        }
    });

    if (allProfiles.length > 0) _startSpriteAnim();
    else _stopSpriteAnim();
}

function _pickWanderTarget(av) {
    const margin = 32;
    const maxX = Math.max(margin, _avatarWorldWidth - 64 - margin);
    let target = margin + Math.floor(Math.random() * (maxX - margin));
    // Don't pick a target too close to current position
    if (Math.abs(target - av.x) < 40) {
        target = av.x + (Math.random() > 0.5 ? 60 : -60);
    }
    av.wanderTarget = Math.max(margin, Math.min(maxX, target));
}

// Desks are tiled every 320px (office_bg_desks.png is 80px native @ 4x scale).
// Monitor centers within each tile: native x=17 and x=57 → screen x=68 and 228.
// Avatar element is 64px wide; visual center = left+32.
// To position avatar centered on monitor: avatar.x = monitorScreenX - 32.
const DESK_TILE_WIDTH = 320;
const DESK_OFFSETS = [68 - 32, 228 - 32];  // = [36, 196]

function _nearestDesk(x) {
    const candidates = [];
    const maxX = _avatarWorldWidth - 64;
    for (let base = 0; base < _avatarWorldWidth + DESK_TILE_WIDTH; base += DESK_TILE_WIDTH) {
        for (const offset of DESK_OFFSETS) {
            const dx = base + offset;
            if (dx >= 0 && dx <= maxX) candidates.push(dx);
        }
    }
    if (!candidates.length) return null;
    // Skip desks already occupied by another avatar
    const taken = Object.values(_avatarState)
        .filter(a => a.state === 'sitting' || a.state === 'walking_to_desk')
        .map(a => a.targetX);
    const free = candidates.filter(c => !taken.some(t => Math.abs(t - c) < 40));
    const pool = free.length ? free : candidates;
    // Pick nearest from pool
    pool.sort((a, b) => Math.abs(a - x) - Math.abs(b - x));
    return pool[0];
}

// ── User typing detection ──────────────────────────────────
let _isUserTyping = false;

function _onUserTyping() {
    _isUserTyping = true;

    // Set wandering avatars to idle while user is typing (no autonomous sitting)
    Object.keys(_avatarState).forEach(profile => {
        const av = _avatarState[profile];
        if (!av) return;
        // Don't disturb avatars actively working (walking_to_desk / sitting)
        if (av.state === 'sitting' || av.state === 'walking_to_desk') return;
        if (av.state === 'wandering' || av.state === 'wander_pause') {
            av.state = 'idle';
        }
    });

    // After user stops typing, resume wandering
    clearTimeout(_typingTimer);
    _typingTimer = setTimeout(() => {
        _isUserTyping = false;
        Object.keys(_avatarState).forEach(profile => {
            const av = _avatarState[profile];
            if (!av) return;
            if (av.state === 'sitting' || av.state === 'walking_to_desk') return;
            if (av.state === 'idle') {
                _pickWanderTarget(av);
                av.state = 'wandering';
            }
        });
    }, 2000);
}

// Hook into terminal input
function _hookTypingDetection() {
    const input = document.getElementById("terminalInlineInput");
    if (input && !input._typingHooked) {
        input.addEventListener("input", _onUserTyping);
        input._typingHooked = true;
    }
}

// Re-hook after DOM changes — called from showTerminalMessages()


// ── Sprite Customization UI ──────────────────────────────────────

// ── Sprite Picker Context Menu (click avatar in 2D world) ───────
let _spritePickerEl = null;

function _openSpritePicker(profile, anchorEl) {
    _closeSpritePicker();
    const picker = document.createElement('div');
    picker.id = 'spritePicker';
    picker.style.cssText = 'position:absolute;z-index:1000;background:var(--surface);border:1px solid var(--border-color);border-radius:8px;padding:8px;box-shadow:0 8px 24px rgba(0,0,0,0.4);display:flex;gap:6px;align-items:center;';
    
    const currentSprite = _profileSpriteMap[profile] || 'office_man';
    
    AGENT_SPRITES.forEach(s => {
        const thumb = document.createElement('div');
        thumb.style.cssText = 'width:32px;height:32px;background:url(assets/' + s + '.png) 0px 0px no-repeat;background-size:128px 128px;image-rendering:pixelated;border-radius:4px;cursor:pointer;border:2px solid ' + (s === currentSprite ? 'var(--primary)' : 'transparent') + ';transition:border-color 0.15s;';
        thumb.title = s;
        thumb.onmouseenter = () => { if (s !== currentSprite) thumb.style.borderColor = 'var(--on-surface-variant)'; };
        thumb.onmouseleave = () => { thumb.style.borderColor = s === currentSprite ? 'var(--primary)' : 'transparent'; };
        thumb.onclick = (e) => {
            e.stopPropagation();
            _profileSpriteMap[profile] = s;
            localStorage.setItem('talaria_profile_sprites', JSON.stringify(_profileSpriteMap));
            _closeSpritePicker();
            // Force avatar refresh
            if (_avatarState[profile]) {
                _avatarState[profile].element.remove();
                delete _avatarState[profile];
            }
            update2DWorld();
        };
        picker.appendChild(thumb);
    });
    
    // Position near avatar
    const world = document.getElementById('agent2DWorld');
    if (world) {
        const worldRect = world.getBoundingClientRect();
        const avatarRect = anchorEl.getBoundingClientRect();
        picker.style.left = (avatarRect.left - worldRect.left + avatarRect.width / 2 - 100) + 'px';
        picker.style.top = (avatarRect.top - worldRect.top - 48) + 'px';
        world.appendChild(picker);
    }
    _spritePickerEl = picker;
}

function _closeSpritePicker() {
    if (_spritePickerEl && _spritePickerEl.parentNode) {
        _spritePickerEl.remove();
    }
    _spritePickerEl = null;
}

// Click avatar in 2D world to open picker
document.addEventListener('click', (e) => {
    const avatar = e.target.closest('.agent-avatar');
    if (avatar) {
        e.stopPropagation();
        const profile = avatar.dataset.profile;
        if (profile) _openSpritePicker(profile, avatar);
        return;
    }
    // Click elsewhere closes picker
    if (!e.target.closest('#spritePicker')) {
        _closeSpritePicker();
    }
});

// Session search filter for panel view
function filterSessions() {
    const query = document.getElementById('sessionsSearchInput')?.value.toLowerCase() || '';
    document.querySelectorAll('#terminalSessionsList .sess-row').forEach(row => {
        const id = row.dataset.sid.toLowerCase();
        const title = row.querySelector('span')?.textContent.toLowerCase() || '';
        row.style.display = (id.includes(query) || title.includes(query)) ? 'flex' : 'none';
    });
}
