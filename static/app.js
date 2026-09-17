/**
 * Dual-Panel Activity & Protocol Visualizer
 * Core Frontend State Manager & Live Protocol Synchronizer
 */

class VisualizerApp {
  constructor() {
    this.currentTrace = null;
    this.currentStepIdx = 0;
    this.isPlaying = false;
    this.playbackInterval = null;
    this.playbackSpeed = 1000;
    this.activeTab = "browsing";
    this.activeVizView = "ladder";
    this.activeInspectorTab = "wire";

    this.videoInterval = null;
    this.videoFrame = 0;
    this.videoBuffered = 0;

    this.initElements();
    this.bindEvents();
    this.initVideoCanvas();

    // Trigger initial default trace so panels are lively immediately
    this.loadBrowsingTrace("wikipedia.org/wiki/Computer_network");
  }

  initElements() {
    // Tabs
    this.tabBtns = document.querySelectorAll(".tab-btn");
    this.views = {
      browsing: document.getElementById("view-browsing"),
      mail: document.getElementById("view-mail"),
      streaming: document.getElementById("view-streaming")
    };

    // Browsing elements
    this.urlInput = document.getElementById("browser-url-input");
    this.btnVisit = document.getElementById("btn-visit-url");
    this.browserDisplayUrl = document.getElementById("txt-active-url");
    this.browserStatusBadge = document.getElementById("browser-status-badge");
    this.browserViewport = document.getElementById("browser-viewport-content");
    this.browseLog = document.getElementById("browse-log-stream");

    // Mail elements
    this.mailFrom = document.getElementById("mail-from");
    this.mailTo = document.getElementById("mail-to");
    this.mailSubject = document.getElementById("mail-subject");
    this.mailBody = document.getElementById("mail-body");
    this.btnSendMail = document.getElementById("btn-send-mail");
    this.mailReceipt = document.getElementById("mail-receipt-card");
    this.mailLog = document.getElementById("mail-log-stream");

    // Streaming elements
    this.btnStreamPlay = document.getElementById("btn-stream-play");
    this.btnStreamPause = document.getElementById("btn-stream-pause");
    this.streamQuality = document.getElementById("stream-quality");
    this.bufferBar = document.getElementById("stream-buffer-bar");
    this.playheadBar = document.getElementById("stream-playhead");
    this.txtBufferTime = document.getElementById("txt-buffer-time");
    this.txtBitrate = document.getElementById("txt-bitrate");
    this.txtOverlayRes = document.getElementById("txt-overlay-res");
    this.bufferingSpinner = document.getElementById("buffering-spinner");
    this.streamLog = document.getElementById("stream-log-stream");
    this.videoCanvas = document.getElementById("video-canvas");

    // Visualizer header controls
    this.btnReplay = document.getElementById("btn-step-replay");
    this.btnPrev = document.getElementById("btn-step-prev");
    this.btnTogglePlay = document.getElementById("btn-toggle-play");
    this.btnNext = document.getElementById("btn-step-next");
    this.playbackSpeedSelect = document.getElementById("playback-speed");
    this.lblActiveFlow = document.getElementById("lbl-active-flow");
    this.lblStepCounter = document.getElementById("lbl-step-counter");

    // View switchers
    this.btnViewLadder = document.getElementById("btn-view-ladder");
    this.btnViewCards = document.getElementById("btn-view-cards");
    this.viewLadderContainer = document.getElementById("view-ladder-container");
    this.viewCardsContainer = document.getElementById("view-cards-container");
    this.ladderMessagesList = document.getElementById("ladder-messages-list");
    this.cardsStreamList = document.getElementById("cards-stream-list");

    // Inspector
    this.inspectorTitle = document.getElementById("inspector-step-title");
    this.insTabs = document.querySelectorAll(".ins-tab");
    this.paneWire = document.getElementById("pane-wire");
    this.paneFields = document.getElementById("pane-fields");
    this.paneRfc = document.getElementById("pane-rfc");
    this.txtRawWire = document.getElementById("txt-raw-wire");
    this.tblFieldsBody = document.getElementById("tbl-fields-body");
    this.serverNodeName = document.getElementById("lbl-server-node-name");
    this.serverNodeIp = document.getElementById("lbl-server-node-ip");
  }

  bindEvents() {
    // Tab switching
    this.tabBtns.forEach(btn => {
      btn.addEventListener("click", () => {
        const targetTab = btn.getAttribute("data-tab");
        this.switchTab(targetTab);
      });
    });

    // Browsing Visit
    this.btnVisit.addEventListener("click", () => {
      this.loadBrowsingTrace(this.urlInput.value);
    });

    this.urlInput.addEventListener("keydown", (e) => {
      if (e.key === "Enter") this.loadBrowsingTrace(this.urlInput.value);
    });

    document.querySelectorAll(".chip[data-url]").forEach(c => {
      c.addEventListener("click", (e) => {
        this.urlInput.value = e.target.getAttribute("data-url");
        this.loadBrowsingTrace(this.urlInput.value);
      });
    });

    // Mail Send
    this.btnSendMail.addEventListener("click", () => {
      this.loadMailTrace(
        this.mailTo.value,
        this.mailSubject.value,
        this.mailBody.value
      );
    });

    document.querySelectorAll(".mail-chip[data-to]").forEach(c => {
      c.addEventListener("click", (e) => {
        this.mailTo.value = e.target.getAttribute("data-to");
      });
    });

    // Streaming Controls
    this.btnStreamPlay.addEventListener("click", () => {
      this.loadStreamingTrace(this.streamQuality.value);
      this.startVideoCanvas();
    });

    this.btnStreamPause.addEventListener("click", () => {
      this.pauseVideoCanvas();
      this.logActivity("stream", "Video playback paused by user.");
    });

    this.streamQuality.addEventListener("change", (e) => {
      const q = e.target.value;
      this.txtOverlayRes.textContent = `${q} ABR`;
      this.logActivity("stream", `Quality switch requested: ${q}. Adaptively retrieving new variant playlist...`);
      this.loadStreamingTrace(q);
    });

    // Playback Toolbar
    this.btnTogglePlay.addEventListener("click", () => this.toggleAutoPlay());
    this.btnNext.addEventListener("click", () => this.stepForward());
    this.btnPrev.addEventListener("click", () => this.stepBackward());
    this.btnReplay.addEventListener("click", () => this.replayTrace());

    this.playbackSpeedSelect.addEventListener("change", (e) => {
      this.playbackSpeed = parseInt(e.target.value, 10);
      if (this.isPlaying) {
        this.stopAutoPlay();
        this.startAutoPlay();
      }
    });

    // View Switcher
    this.btnViewLadder.addEventListener("click", () => this.switchVizView("ladder"));
    this.btnViewCards.addEventListener("click", () => this.switchVizView("cards"));

    // Inspector Tabs
    this.insTabs.forEach(tab => {
      tab.addEventListener("click", () => {
        this.insTabs.forEach(t => t.classList.remove("active"));
        tab.classList.add("active");
        const insType = tab.getAttribute("data-ins");
        this.showInspectorPane(insType);
      });
    });

    // Clear logs
    document.getElementById("clear-browse-log").addEventListener("click", () => this.browseLog.innerHTML = "");
    document.getElementById("clear-mail-log").addEventListener("click", () => this.mailLog.innerHTML = "");
    document.getElementById("clear-stream-log").addEventListener("click", () => this.streamLog.innerHTML = "");
  }

  switchTab(tab) {
    this.activeTab = tab;
    this.tabBtns.forEach(b => b.classList.toggle("active", b.getAttribute("data-tab") === tab));
    Object.keys(this.views).forEach(k => {
      this.views[k].classList.toggle("active", k === tab);
    });

    if (tab === "browsing") {
      this.loadBrowsingTrace(this.urlInput.value);
    } else if (tab === "mail") {
      this.loadMailTrace(this.mailTo.value, this.mailSubject.value, this.mailBody.value);
    } else if (tab === "streaming") {
      this.loadStreamingTrace(this.streamQuality.value);
    }
  }

  switchVizView(view) {
    this.activeVizView = view;
    this.btnViewLadder.classList.toggle("active", view === "ladder");
    this.btnViewCards.classList.toggle("active", view === "cards");
    this.viewLadderContainer.style.display = view === "ladder" ? "block" : "none";
    this.viewCardsContainer.style.display = view === "cards" ? "block" : "none";
  }

  showInspectorPane(pane) {
    this.activeInspectorTab = pane;
    this.paneWire.classList.toggle("active", pane === "wire");
    this.paneFields.classList.toggle("active", pane === "fields");
    this.paneRfc.classList.toggle("active", pane === "rfc");
  }

  logActivity(category, message) {
    const entry = document.createElement("div");
    entry.className = "log-entry";
    const ts = new Date().toLocaleTimeString();
    entry.textContent = `[${ts}] ${message}`;

    let target = this.browseLog;
    if (category === "mail") target = this.mailLog;
    if (category === "stream") target = this.streamLog;

    target.appendChild(entry);
    target.scrollTop = target.scrollHeight;
  }

  /* ------------------------------------------------------------- */
  /* TRACE LOADERS (FETCH FROM BACKEND API)                        */
  /* ------------------------------------------------------------- */
  async loadBrowsingTrace(url) {
    this.stopAutoPlay();
    this.browserDisplayUrl.textContent = "https://" + url.replace(/^https?:\/\//, "");
    this.browserStatusBadge.textContent = "Resolving DNS...";
    this.browserStatusBadge.style.color = "#a855f7";
    this.logActivity("browse", `User requested URL: ${url}. Initiating DNS lookup...`);

    try {
      const resp = await fetch(`/api/protocols/browse?url=${encodeURIComponent(url)}`);
      const data = await resp.json();
      this.currentTrace = data;
      this.serverNodeName.textContent = "Web Server (" + data.host + ")";
      this.serverNodeIp.textContent = data.server_ip + ":" + data.port;
      this.lblActiveFlow.textContent = `Browsing: ${data.host} (DNS → HTTP)`;

      this.renderTraceVisualizations();
      this.startAutoPlay();
    } catch (err) {
      console.error(err);
      this.logActivity("browse", "Failed to fetch protocol trace from server.");
    }
  }

  async loadMailTrace(to, subject, body) {
    this.stopAutoPlay();
    this.mailReceipt.style.display = "none";
    this.logActivity("mail", `Drafting email to <${to}>. Querying MX records...`);

    try {
      const resp = await fetch("/api/protocols/mail", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ to, subject, body })
      });
      const data = await resp.json();
      this.currentTrace = data;
      this.serverNodeName.textContent = "Mail Server (" + data.mx_host + ")";
      this.serverNodeIp.textContent = data.mx_ip + ":25 (SMTP)";
      this.lblActiveFlow.textContent = `Mail: <${data.to}> (DNS MX → SMTP)`;

      this.renderTraceVisualizations();
      this.startAutoPlay();
    } catch (err) {
      console.error(err);
      this.logActivity("mail", "Failed to fetch mail protocol trace.");
    }
  }

  async loadStreamingTrace(quality) {
    this.stopAutoPlay();
    this.bufferingSpinner.style.display = "flex";
    this.logActivity("stream", `Starting stream session. Target variant: ${quality}.`);

    try {
      const resp = await fetch(`/api/protocols/stream?quality=${encodeURIComponent(quality)}`);
      const data = await resp.json();
      this.currentTrace = data;
      this.serverNodeName.textContent = "Media CDN Edge";
      this.serverNodeIp.textContent = "104.22.41.98:443 (HLS)";
      this.lblActiveFlow.textContent = `Streaming: ${quality} (DNS → HLS Master/Chunks)`;
      this.txtBitrate.textContent = `${data.bitrate_kbps.toLocaleString()} kbps`;

      this.renderTraceVisualizations();
      this.startAutoPlay();
    } catch (err) {
      console.error(err);
      this.logActivity("stream", "Failed to fetch streaming protocol trace.");
    }
  }

  /* ------------------------------------------------------------- */
  /* RENDER PROTOCOL VISUALIZATIONS                                */
  /* ------------------------------------------------------------- */
  renderTraceVisualizations() {
    this.currentStepIdx = 0;
    this.ladderMessagesList.innerHTML = "";
    this.cardsStreamList.innerHTML = "";

    if (!this.currentTrace || !this.currentTrace.steps) return;

    const steps = this.currentTrace.steps;
    this.lblStepCounter.textContent = `Step 1 / ${steps.length}`;

    // Render Ladder Rows
    steps.forEach((step, idx) => {
      const row = document.createElement("div");
      row.className = "ladder-msg-row";
      row.id = `ladder-step-${idx}`;
      row.setAttribute("data-step", idx);

      let leftPct = "16.6%";
      let widthPct = "33.3%";
      let isRightArrow = true;

      if (step.direction === "client_to_dns") {
        leftPct = "16.6%";
        widthPct = "33.3%";
        isRightArrow = true;
      } else if (step.direction === "dns_to_client") {
        leftPct = "16.6%";
        widthPct = "33.3%";
        isRightArrow = false;
      } else if (step.direction === "client_to_server") {
        leftPct = "16.6%";
        widthPct = "66.6%";
        isRightArrow = true;
      } else if (step.direction === "server_to_client") {
        leftPct = "16.6%";
        widthPct = "66.6%";
        isRightArrow = false;
      }

      const arrowLine = document.createElement("div");
      arrowLine.className = "arrow-line";
      arrowLine.style.left = leftPct;
      arrowLine.style.width = widthPct;

      const arrowHead = document.createElement("div");
      arrowHead.className = `arrow-head ${isRightArrow ? "arrow-right" : "arrow-left"}`;
      arrowLine.appendChild(arrowHead);

      const bubble = document.createElement("div");
      bubble.className = "msg-label-bubble";
      bubble.textContent = `#${step.step_id} [${step.protocol}] ${step.title}`;
      arrowLine.appendChild(bubble);

      row.appendChild(arrowLine);
      row.addEventListener("click", () => this.jumpToStep(idx));
      this.ladderMessagesList.appendChild(row);

      // Render Chronological Card
      const card = document.createElement("div");
      card.className = "proto-card";
      card.id = `card-step-${idx}`;
      card.setAttribute("data-step", idx);

      card.innerHTML = `
        <div class="card-step-num">#${step.step_id}</div>
        <div class="card-body">
          <div class="card-top-row">
            <span class="proto-pill proto-pill-${step.protocol}">${step.protocol}</span>
            <span class="card-timing">+${step.time_offset_ms}ms</span>
          </div>
          <div class="card-title">${step.title}</div>
          <div class="card-summary">${step.summary}</div>
        </div>
      `;
      card.addEventListener("click", () => this.jumpToStep(idx));
      this.cardsStreamList.appendChild(card);
    });

    this.highlightActiveStep(0);
  }

  /* ------------------------------------------------------------- */
  /* STEP PLAYBACK & SYNCHRONIZATION WITH LEFT PANEL               */
  /* ------------------------------------------------------------- */
  highlightActiveStep(idx) {
    if (!this.currentTrace || !this.currentTrace.steps[idx]) return;
    this.currentStepIdx = idx;
    const step = this.currentTrace.steps[idx];
    const total = this.currentTrace.steps.length;

    this.lblStepCounter.textContent = `Step ${idx + 1} / ${total}`;

    // Highlight Ladder row
    document.querySelectorAll(".ladder-msg-row").forEach(r => r.classList.remove("active-step"));
    const activeLadder = document.getElementById(`ladder-step-${idx}`);
    if (activeLadder) {
      activeLadder.classList.add("active-step");
      activeLadder.scrollIntoView({ behavior: "smooth", block: "nearest" });
    }

    // Highlight Card
    document.querySelectorAll(".proto-card").forEach(c => c.classList.remove("active-step"));
    const activeCard = document.getElementById(`card-step-${idx}`);
    if (activeCard) {
      activeCard.classList.add("active-step");
      activeCard.scrollIntoView({ behavior: "smooth", block: "nearest" });
    }

    // Update Deep Inspector
    this.inspectStep(step);

    // Live Synchronization with Left Panel
    this.syncLeftPanelWithStep(step, idx, total);
  }

  syncLeftPanelWithStep(step, idx, total) {
    const activity = this.currentTrace.activity;

    if (activity === "browsing") {
      if (step.protocol === "DNS") {
        this.browserStatusBadge.textContent = "DNS Resolving...";
        this.browserStatusBadge.style.color = "#a855f7";
        this.logActivity("browse", `DNS query for ${this.currentTrace.host}`);
      } else if (step.protocol === "TCP") {
        this.browserStatusBadge.textContent = "TCP Handshake...";
        this.browserStatusBadge.style.color = "#38bdf8";
        this.logActivity("browse", "TCP 3-way handshake established on port " + this.currentTrace.port);
      } else if (step.protocol === "HTTP" && step.direction === "client_to_server") {
        this.browserStatusBadge.textContent = "HTTP GET Request Sent...";
        this.browserStatusBadge.style.color = "#3b82f6";
        this.logActivity("browse", "HTTP GET dispatched to web server.");
      } else if (step.protocol === "HTTP" && step.direction === "server_to_client") {
        this.browserStatusBadge.textContent = "200 OK (Loaded)";
        this.browserStatusBadge.style.color = "#10b981";
        this.browserViewport.innerHTML = this.currentTrace.rendered_content;
        this.logActivity("browse", "HTML payload rendered into browser viewport.");
      }
    } else if (activity === "mail") {
      if (step.protocol === "DNS") {
        this.logActivity("mail", `Looking up MX host ${this.currentTrace.mx_host}`);
      } else if (step.protocol === "SMTP") {
        if (step.title.includes("EHLO")) {
          this.logActivity("mail", "Client greeting: EHLO mailclient.local");
        } else if (step.title.includes("MAIL FROM")) {
          this.logActivity("mail", `Envelope sender configured: <${this.currentTrace.from}>`);
        } else if (step.title.includes("RCPT TO")) {
          this.logActivity("mail", `Envelope recipient configured: <${this.currentTrace.to}>`);
        } else if (step.title.includes("DATA")) {
          this.logActivity("mail", "Transmitting RFC 5322 payload...");
        } else if (step.title.includes("250 Queued")) {
          this.mailReceipt.style.display = "block";
          document.getElementById("rcpt-mx-host").textContent = this.currentTrace.mx_host;
          document.getElementById("rcpt-queue-id").textContent = this.currentTrace.queue_id;
          this.logActivity("mail", `Server accepted message! Spooled as ID ${this.currentTrace.queue_id}`);
        } else if (step.title.includes("QUIT")) {
          this.logActivity("mail", "SMTP conversation completed. Channel closed.");
        }
      }
    } else if (activity === "streaming") {
      if (step.title.includes("Master Manifest")) {
        this.logActivity("stream", "Master manifest received. Adaptive multi-bitrates loaded.");
      } else if (step.title.includes("Media Playlist")) {
        this.logActivity("stream", `Media playlist for ${this.currentTrace.quality} loaded.`);
      } else if (step.title.includes("Chunk Delivered")) {
        this.bufferingSpinner.style.display = "none";
        this.videoBuffered = Math.min(16.0, this.videoBuffered + 4.0);
        const pct = (this.videoBuffered / 16.0) * 100;
        this.bufferBar.style.width = `${pct}%`;
        this.txtBufferTime.textContent = `${this.videoBuffered.toFixed(1)}s`;
        this.logActivity("stream", `Delivered segment chunk. Buffer increased to ${this.videoBuffered.toFixed(1)}s`);
      }
    }
  }

  inspectStep(step) {
    this.inspectorTitle.textContent = `Step #${step.step_id}: ${step.title}`;
    this.txtRawWire.textContent = step.raw_wire;

    // Fields table
    this.tblFieldsBody.innerHTML = "";
    Object.entries(step.key_fields).forEach(([k, v]) => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td style="font-weight:600; color:#93c5fd;">${k}</td>
        <td><code>${v}</code></td>
        <td style="color:#94a3b8;">${this.getFieldExplanation(k, v)}</td>
      `;
      this.tblFieldsBody.appendChild(tr);
    });
  }

  getFieldExplanation(key, val) {
    const dict = {
      "Method": "HTTP request verb defined in RFC 7231 (e.g. GET retrieves resource)",
      "Status Code": "RFC 7231 response code (200 OK signals resource delivery)",
      "Transaction ID": "16-bit identifier matched between DNS query and response (RFC 1035)",
      "Query Type": "DNS Record type (A = IPv4 Address, MX = Mail Exchange Server)",
      "Reply Code": "RFC 5321 3-digit reply code (250 = requested mail action completed)",
      "Command": "SMTP client action verb (EHLO, MAIL FROM, RCPT TO, DATA, QUIT)",
      "TTL": "Time to Live in seconds before DNS cache must invalidate",
      "Range Support": "HTTP 1.1 byte-serving header enabling partial chunk streaming"
    };
    return dict[key] || "Protocol parameter specified by Application Layer RFC standards";
  }

  /* ------------------------------------------------------------- */
  /* PLAYBACK CONTROLS                                             */
  /* ------------------------------------------------------------- */
  stepForward() {
    if (!this.currentTrace || !this.currentTrace.steps) return;
    if (this.currentStepIdx < this.currentTrace.steps.length - 1) {
      this.highlightActiveStep(this.currentStepIdx + 1);
    } else {
      this.stopAutoPlay();
    }
  }

  stepBackward() {
    if (!this.currentTrace || !this.currentTrace.steps) return;
    if (this.currentStepIdx > 0) {
      this.highlightActiveStep(this.currentStepIdx - 1);
    }
  }

  jumpToStep(idx) {
    this.stopAutoPlay();
    this.highlightActiveStep(idx);
  }

  replayTrace() {
    this.stopAutoPlay();
    this.videoBuffered = 0;
    this.bufferBar.style.width = "0%";
    this.txtBufferTime.textContent = "0.0s";
    this.highlightActiveStep(0);
    this.startAutoPlay();
  }

  toggleAutoPlay() {
    if (this.isPlaying) {
      this.stopAutoPlay();
    } else {
      this.startAutoPlay();
    }
  }

  startAutoPlay() {
    this.isPlaying = true;
    this.btnTogglePlay.textContent = "⏸ Pause";
    this.btnTogglePlay.classList.add("active-pulse");

    if (this.currentStepIdx >= (this.currentTrace?.steps?.length || 1) - 1) {
      this.currentStepIdx = 0;
      this.highlightActiveStep(0);
    }

    if (this.playbackInterval) clearInterval(this.playbackInterval);
    this.playbackInterval = setInterval(() => {
      if (!this.currentTrace || !this.currentTrace.steps) {
        this.stopAutoPlay();
        return;
      }
      if (this.currentStepIdx < this.currentTrace.steps.length - 1) {
        this.stepForward();
      } else {
        this.stopAutoPlay();
      }
    }, this.playbackSpeed);
  }

  stopAutoPlay() {
    this.isPlaying = false;
    this.btnTogglePlay.textContent = "▶ Auto";
    this.btnTogglePlay.classList.remove("active-pulse");
    if (this.playbackInterval) {
      clearInterval(this.playbackInterval);
      this.playbackInterval = null;
    }
  }

  /* ------------------------------------------------------------- */
  /* VIDEO CANVAS SIMULATOR                                        */
  /* ------------------------------------------------------------- */
  initVideoCanvas() {
    const ctx = this.videoCanvas.getContext("2d");
    ctx.fillStyle = "#0f172a";
    ctx.fillRect(0, 0, 480, 240);
    ctx.fillStyle = "#64748b";
    ctx.font = "14px Inter, sans-serif";
    ctx.textAlign = "center";
    ctx.fillText("Video Buffer Ready - Click Play to Stream HLS Chunks", 240, 120);
  }

  startVideoCanvas() {
    if (this.videoInterval) clearInterval(this.videoInterval);
    const ctx = this.videoCanvas.getContext("2d");

    let playheadSec = 0;
    this.videoInterval = setInterval(() => {
      this.videoFrame++;
      playheadSec += 0.1;
      if (playheadSec > 16.0) playheadSec = 0;
      const playPct = (playheadSec / 16.0) * 100;
      this.playheadBar.style.width = `${playPct}%`;

      ctx.fillStyle = "#090d16";
      ctx.fillRect(0, 0, 480, 240);

      ctx.beginPath();
      ctx.lineWidth = 3;
      ctx.strokeStyle = "#38bdf8";
      for (let x = 0; x < 480; x += 5) {
        const y = 120 + Math.sin((x + this.videoFrame * 4) * 0.04) * 45;
        if (x === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
      }
      ctx.stroke();

      ctx.fillStyle = "#ffffff";
      ctx.font = "bold 16px Fira Code, monospace";
      ctx.textAlign = "center";
      ctx.fillText("HLS Transport Stream: Active", 240, 60);

      ctx.fillStyle = "#94a3b8";
      ctx.font = "12px Fira Code, monospace";
      ctx.fillText(`Frame #${this.videoFrame} · Codec: H.264/AVC · PTS: ${(this.videoFrame / 30).toFixed(2)}s`, 240, 190);
    }, 100);
  }

  pauseVideoCanvas() {
    if (this.videoInterval) {
      clearInterval(this.videoInterval);
      this.videoInterval = null;
    }
  }
}

document.addEventListener("DOMContentLoaded", () => {
  window.app = new VisualizerApp();
});
