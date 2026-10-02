// ============================================================
// CN Protocol Visualizer - Frontend JavaScript
// Application Layer + Transport Layer
// ============================================================

let currentMode = "browsing";
let steps = [];
let currentStep = -1;
let timer = null;
let vizPlaying = false;

const $ = (id) => document.getElementById(id);

const labels = {
    browsing: "DNS (UDP) + TCP + HTTP",
    mail: "DNS + TCP + SMTP",
    streaming: "DNS + TCP + HLS Streaming",
    transport: "TCP 3-Way Handshake & Teardown"
};

// Protocol colour / display config
const PROTO_COLORS = {
    DNS:  { color: "#a855f7", bg: "rgba(168,85,247,0.18)", border: "#a855f7" },
    HTTP: { color: "#3b82f6", bg: "rgba(59,130,246,0.18)",  border: "#3b82f6" },
    SMTP: { color: "#f59e0b", bg: "rgba(245,158,11,0.18)",  border: "#f59e0b" },
    TCP:  { color: "#94a3b8", bg: "rgba(100,116,139,0.18)", border: "#64748b" },
    HLS:  { color: "#10b981", bg: "rgba(16,185,129,0.18)",  border: "#10b981" },
};

// Layer label per protocol
const LAYER_LABELS = {
    DNS:  "Application Layer (L7) — DNS over UDP/53",
    HTTP: "Application Layer (L7) — HTTP/HTTPS",
    SMTP: "Application Layer (L7) — SMTP (RFC 5321)",
    TCP:  "Transport Layer (L4) — TCP Segment",
    HLS:  "Application Layer (L7) — HLS over HTTP",
};

// Key-field section header
const FIELD_LABELS = {
    DNS:  "DNS Header / Key Fields",
    HTTP: "HTTP Header / Key Fields",
    SMTP: "SMTP Command / Key Fields",
    TCP:  "TCP Segment / Key Fields",
    HLS:  "HLS Manifest / Key Fields",
};


// ============================================================
// Activity Log
// ============================================================

function addLog(text) {
    const box = $("activityLog");

    if (!box) return;

    const empty = box.querySelector(".empty");

    if (empty) {
        empty.remove();
    }

    const item = document.createElement("div");

    item.className = "log-item";

    item.innerHTML = `
        <time>${new Date().toLocaleTimeString()}</time>
        ${escapeHtml(text)}
    `;

    box.prepend(item);
}


// ============================================================
// HTML Escape
// ============================================================

function escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text ?? "";
    return div.innerHTML;
}


// ============================================================
// Tab Switching
// ============================================================

document.querySelectorAll(".tab").forEach(btn => {

    btn.addEventListener("click", () => {
        switchMode(btn.dataset.mode);
    });

});


function switchMode(mode) {

    currentMode = mode;

    document.querySelectorAll(".tab").forEach(btn => {
        btn.classList.toggle(
            "active",
            btn.dataset.mode === mode
        );
    });

    [
        "browsing",
        "mail",
        "streaming",
        "transport"
    ].forEach(m => {

        const box = $(m + "Box");

        if (box) {
            box.classList.toggle(
                "hidden",
                m !== mode
            );
        }

    });

    resetVisualizer();

    addLog(
        `Switched mode to ${mode.toUpperCase()}.`
    );
}


// ============================================================
// Normal Application Activity
// Browsing / Mail / Streaming
// ============================================================

async function runActivity(activity, logText, extraParams = {}) {

    try {

        addLog(logText);

        const includeTransport =
            $("includeTransportToggle")
                ? $("includeTransportToggle").checked
                : true;

        const response = await fetch(
            "/api/simulate",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    activity: activity,
                    include_transport: includeTransport,
                    ...extraParams
                })
            }
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.error || "Simulation failed"
            );
        }

        steps = Array.isArray(data.steps)
            ? data.steps
            : [];

        if (!steps.length) {
            throw new Error(
                "No simulation steps received."
            );
        }

        currentStep = 0;

        $("protocolName").textContent =
            labels[activity] || activity.toUpperCase();

        setStatusOnline();

        enableControls();

        renderStep();

        startAutoReveal();

    } catch (err) {

        addLog(
            "Error: " + err.message
        );

        console.error(err);
    }
}


// ============================================================
// Status
// ============================================================

function setStatusOnline() {

    const statusDot = $("statusDot");

    if (!statusDot) return;

    statusDot.style.background = "#31d59b";

    statusDot.style.boxShadow =
        "0 0 14px #31d59b";
}


// ============================================================
// 1. Browsing
// ============================================================

const visitBtn = $("visitBtn");

if (visitBtn) {

    visitBtn.addEventListener(
        "click",
        () => {

            const url =
                $("urlInput").value.trim()
                || "https://example.com";

            addLog(
                `Initiated visit to ${url}.`
            );

            runActivity(
                "browsing",
                `Browsing trace started for ${url}.`,
                { url }
            );

        }
    );
}


// ============================================================
// 2. Mail
// ============================================================

const sendBtn = $("sendBtn");

if (sendBtn) {

    sendBtn.addEventListener(
        "click",
        () => {

            const to =
                $("toInput").value.trim()
                || "receiver@example.net";

            const subject =
                $("subjectInput").value.trim()
                || "Assignment Demo";

            const body =
                $("bodyInput")
                    ? $("bodyInput").value.trim()
                    : "";

            addLog(
                `Mail drafted for ${to} - "${subject}".`
            );

            runActivity(
                "mail",
                `SMTP mail transfer initiated for ${to}.`,
                { to, subject, body }
            );

        }
    );
}


// ============================================================
// 3. Streaming
// ============================================================

const playBtn = $("playBtn");

if (playBtn) {

    playBtn.addEventListener(
        "click",
        () => {

            // The select option may include a label like "720p (HD 2.8 Mbps)"
            // Extract just the resolution prefix for the backend
            const rawQuality =
                $("qualitySelect").value;

            const quality =
                rawQuality.split(" ")[0] || "720p";

            $("streamState").textContent =
                `Streaming at ${quality}`;

            addLog(
                `Video stream started at ${quality}.`
            );

            runActivity(
                "streaming",
                `HLS adaptive stream initiated at ${quality}.`,
                { quality }
            );

        }
    );
}


const pauseBtn = $("pauseBtn");

if (pauseBtn) {

    pauseBtn.addEventListener(
        "click",
        () => {

            $("streamState").textContent =
                "Paused";

            addLog(
                "Stream paused by user."
            );

            stopVizTimer();

        }
    );
}


// ============================================================
// 4. Transport Layer Simulation
// ============================================================

const runTransportBtn =
    $("runTransportBtn");

if (runTransportBtn) {

    runTransportBtn.addEventListener(
        "click",
        async () => {

            try {

                const src =
                    Number(
                        $("srcPort").value
                    ) || 54122;

                const dst =
                    Number(
                        $("dstPort").value
                    ) || 443;


                const scenarioSelect =
                    $("transportMode");

                const scenario =
                    scenarioSelect
                        ? scenarioSelect.value
                        : "handshake";


                addLog(
                    `Transport Layer simulation started (${src} -> ${dst}).`
                );


                const response =
                    await fetch(
                        "/api/protocols/transport",
                        {
                            method: "POST",

                            headers: {
                                "Content-Type":
                                    "application/json"
                            },

                            body: JSON.stringify({
                                scenario: scenario,
                                src_port: src,
                                dst_port: dst
                            })
                        }
                    );


                const data =
                    await response.json();


                if (!response.ok) {

                    throw new Error(
                        data.error ||
                        "Transport simulation failed"
                    );

                }


                // Backend returns:
                // { steps: [...] }

                steps =
                    Array.isArray(data.steps)
                        ? data.steps
                        : [];


                if (!steps.length) {

                    throw new Error(
                        "No transport simulation steps received."
                    );

                }


                currentStep = 0;


                $("protocolName").textContent =
                    "TCP Transport Layer";


                setStatusOnline();

                enableControls();

                renderStep();


                addLog(
                    `Transport simulation completed: ${steps.length} steps.`
                );


                startAutoReveal();


            } catch (error) {

                console.error(error);

                addLog(
                    `Error: ${error.message}`
                );

            }

        }
    );
}


// ============================================================
// Auto Reveal
// ============================================================

function startAutoReveal() {

    stopVizTimer();

    if (!steps.length) return;

    vizPlaying = true;

    if ($("playVizBtn")) {
        $("playVizBtn").textContent =
            "⏸ Pause";
    }


    timer = setInterval(
        () => {

            if (
                currentStep <
                steps.length - 1
            ) {

                currentStep++;

                renderStep();

            } else {

                stopVizTimer();

            }

        },
        1300
    );
}


// ============================================================
// Stop Auto Reveal
// ============================================================

function stopVizTimer() {

    if (timer) {
        clearInterval(timer);
    }

    timer = null;

    vizPlaying = false;

    if ($("playVizBtn")) {

        $("playVizBtn").textContent =
            "▶ Auto";

    }
}


// ============================================================
// Visualizer Controls
// ============================================================

const playVizBtn = $("playVizBtn");

if (playVizBtn) {

    playVizBtn.addEventListener(
        "click",
        () => {

            if (!steps.length) return;

            if (vizPlaying) {

                stopVizTimer();

            } else {

                startAutoReveal();

            }

        }
    );
}


// ============================================================
// Next
// ============================================================

const nextBtn = $("nextBtn");

if (nextBtn) {

    nextBtn.addEventListener(
        "click",
        () => {

            if (
                currentStep <
                steps.length - 1
            ) {

                currentStep++;

                renderStep();

            }

        }
    );
}


// ============================================================
// Previous
// ============================================================

const prevBtn = $("prevBtn");

if (prevBtn) {

    prevBtn.addEventListener(
        "click",
        () => {

            if (currentStep > 0) {

                currentStep--;

                renderStep();

            }

        }
    );
}


// ============================================================
// Replay
// ============================================================

const replayBtn = $("replayBtn");

if (replayBtn) {

    replayBtn.addEventListener(
        "click",
        () => {

            if (!steps.length) return;

            stopVizTimer();

            currentStep = 0;

            renderStep();

            startAutoReveal();

        }
    );
}


// ============================================================
// Enable Controls
// ============================================================

function enableControls() {

    if ($("prevBtn")) {
        $("prevBtn").disabled = false;
    }

    if ($("nextBtn")) {
        $("nextBtn").disabled = false;
    }

    if ($("playVizBtn")) {
        $("playVizBtn").disabled = false;
    }

    if ($("replayBtn")) {
        $("replayBtn").disabled = false;
    }
}


// ============================================================
// Reset Visualizer
// ============================================================

function resetVisualizer() {

    stopVizTimer();

    steps = [];

    currentStep = -1;


    if ($("protocolName")) {
        $("protocolName").textContent =
            "Waiting";
    }


    if ($("stepCounter")) {
        $("stepCounter").textContent =
            "Step 0 / 0";
    }


    if ($("stepTitle")) {
        $("stepTitle").textContent =
            "Perform an activity to begin.";
    }


    if ($("directionBadge")) {
        $("directionBadge").textContent =
            "Idle";
    }


    if ($("timelineFill")) {
        $("timelineFill").style.width =
            "0%";
    }


    if ($("stepCard")) {

        $("stepCard").className =
            "step-card empty-card";

        $("stepCard").innerHTML = `
            <div class="empty-visual">

                <div class="big-network">
                    ⚡
                </div>

                <h3>
                    Protocol & Transport flow
                    will appear here
                </h3>

                <p>
                    The right panel updates
                    when you perform an activity
                    on the left.
                </p>

            </div>
        `;

    }


    if ($("prevBtn")) {
        $("prevBtn").disabled = true;
    }

    if ($("nextBtn")) {
        $("nextBtn").disabled = true;
    }

    if ($("playVizBtn")) {
        $("playVizBtn").disabled = true;
    }

    if ($("replayBtn")) {
        $("replayBtn").disabled = true;
    }
}


// ============================================================
// Render Step
// Works for all protocols: DNS, HTTP, SMTP, TCP, HLS
// direction values:
//   client_to_server | server_to_client
//   client_to_dns    | dns_to_client
// ============================================================

function renderStep() {

    const s = steps[currentStep];

    if (!s) return;


    const protocol =
        s.protocol || "TCP";

    const title =
        s.title || "Protocol Step";

    const direction =
        s.direction || "";

    const summary =
        s.summary || "";

    const keyFields =
        s.key_fields || {};

    const time =
        s.time_offset_ms ?? 0;

    const sender   = s.sender   || "Client";
    const receiver = s.receiver || "Server";

    // Look up protocol theming (default to TCP grey)
    const theme = PROTO_COLORS[protocol] || PROTO_COLORS["TCP"];
    const layerLabel  = LAYER_LABELS[protocol]  || "Application Layer (L7)";
    const fieldHeader = FIELD_LABELS[protocol]  || "Key Fields";


    // Step counter

    if ($("stepCounter")) {

        $("stepCounter").textContent =
            `Step ${currentStep + 1} / ${steps.length}`;

    }


    // Title

    if ($("stepTitle")) {

        $("stepTitle").textContent =
            title;

    }


    // Direction badge — handle all 4 direction values

    let directionText = "Idle";
    let arrowClass    = "arrow-c2s";

    if (direction === "client_to_server") {
        directionText = "Client → Server";
        arrowClass    = "arrow-c2s";
    } else if (direction === "server_to_client") {
        directionText = "Server → Client";
        arrowClass    = "arrow-s2c";
    } else if (direction === "client_to_dns") {
        directionText = "Client → DNS Resolver";
        arrowClass    = "arrow-c2s";
    } else if (direction === "dns_to_client") {
        directionText = "DNS Resolver → Client";
        arrowClass    = "arrow-s2c";
    }

    if ($("directionBadge")) {
        $("directionBadge").textContent = directionText;
    }


    // Timeline

    if ($("timelineFill")) {
        $("timelineFill").style.width =
            `${((currentStep + 1) / steps.length) * 100}%`;
    }


    // Key fields — build coloured badge list

    let fieldsHTML = "";

    Object.entries(keyFields).forEach(([key, value]) => {
        fieldsHTML += `
            <span class="tag-hl" style="border-color:${theme.border};color:${theme.color}">
                <b>${escapeHtml(key)}:</b>&nbsp;${escapeHtml(String(value))}
            </span>
        `;
    });


    // Arrow label — sender ──▶ receiver

    const arrowLabel =
        (arrowClass === "arrow-c2s")
            ? `${escapeHtml(sender)} ──▶ ${escapeHtml(receiver)}`
            : `${escapeHtml(sender)} ──▶ ${escapeHtml(receiver)}`;


    // Main card — rendered with protocol-correct theming

    if ($("stepCard")) {

        $("stepCard").className = "step-card";
        $("stepCard").style.borderColor = theme.border;
        $("stepCard").style.background  =
            `linear-gradient(135deg, #111827 85%, ${theme.bg})`;

        $("stepCard").innerHTML = `

            <div class="step-top">

                <div class="step-type" style="
                    background:${theme.bg};
                    color:${theme.color};
                    border:1px solid ${theme.border};
                    padding:3px 10px;
                    border-radius:9999px;
                    font-size:11px;
                    font-weight:700;
                    font-family:var(--font-mono);
                    letter-spacing:0.5px;
                ">
                    ${escapeHtml(protocol)}
                </div>

                <div class="time" style="color:${theme.color}">
                    +${escapeHtml(String(time))} ms
                </div>

            </div>


            <h3 style="margin:10px 0 6px">
                ${escapeHtml(title)}
            </h3>


            <div class="arrow ${arrowClass}" style="
                background:${theme.bg};
                border:1px solid ${theme.border};
                border-radius:6px;
                padding:6px 12px;
                font-family:var(--font-mono);
                font-size:12px;
                color:${theme.color};
                word-break:break-all;
            ">
                ${arrowLabel}
            </div>


            <div class="message" style="margin:10px 0">
                ${escapeHtml(summary)}
            </div>


            <div class="step-footer">

                <p style="margin-bottom:8px">
                    <strong style="color:${theme.color}">Layer:</strong>
                    ${escapeHtml(layerLabel)}
                </p>

                <p>
                    <strong style="color:${theme.color}">
                        ${escapeHtml(fieldHeader)}:
                    </strong>
                    <br><br>
                    <span style="display:flex;flex-wrap:wrap;gap:6px;margin-top:4px">
                        ${fieldsHTML}
                    </span>
                </p>

            </div>

        `;

    }


    // TCP State Badge — update whenever a step carries TCP State info

    const tcpStateBadge = $("tcpStateBadge");

    if (tcpStateBadge) {

        if (keyFields["TCP State"]) {

            const state = String(keyFields["TCP State"]);
            tcpStateBadge.textContent = state;

            if (state === "ESTABLISHED") {
                tcpStateBadge.style.background = "#059669";
            } else if (state === "CLOSED" || state.includes("CLOSED")) {
                tcpStateBadge.style.background = "#4b5563";
            } else if (state.includes("WAIT") || state.includes("FIN")) {
                tcpStateBadge.style.background = "#d97706";
            } else {
                tcpStateBadge.style.background = "#2563eb";
            }

        } else if (currentStep === 0 && protocol !== "TCP") {
            // Non-transport activity: show a neutral label
            tcpStateBadge.textContent = "N/A";
            tcpStateBadge.style.background = "#374151";
        }

    }

}




// ============================================================
// Start in Reset State
// ============================================================

resetVisualizer();