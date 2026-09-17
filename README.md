# Dual-Panel Activity & Protocol Visualizer
**Computer Networks – Application Layer Assignment**  
*Built with Google Antigravity & Gemini 3.8 Flash*

A real-time dual-panel web dashboard that allows users to perform common application-layer activities (**Browsing**, **Mail**, and **Streaming**) while simultaneously visualizing the underlying protocol exchanges (**DNS**, **HTTP**, **SMTP**, **HLS**) with step-by-step playback, ladder sequence diagrams, and deep wire packet inspection.

---

## 🌟 Key Features

### 1. Strict Dual-Panel Architecture
- **Left Panel (Activity Panel):**
  - **Web Browsing:** Input any URL, pick quick presets (e.g. `wikipedia.org`, `ietf.org`), and observe simulated DNS resolution, TCP handshake, HTTP request, and rendered HTML page preview.
  - **Mail Client:** Compose email with From, To, Subject, and Body. Sends via simulated SMTP with MX record lookup, envelope negotiation, and spool receipt.
  - **Video Streaming:** Play/pause simulated HLS stream, switch quality variants (1080p, 720p, 480p, 360p), and watch buffer gauge and animated video pattern canvas update dynamically.
  - **Live Client Activity Logs:** Timestamped event feed for each application mode.

- **Right Panel (Protocol Visualization Panel):**
  - **Live Synchronization:** Every action on the left immediately triggers the corresponding protocol sequence on the right.
  - **Playback Controls:** Auto-play with adjustable speed (0.5x, 1x, 2x), Pause, Step Forward, Step Backward, and Replay.
  - **Dual Visualization Modes:**
    1. **Interactive Sequence Ladder Diagram:** Shows Client, DNS Resolver, and Server lifelines with animated directional message arrows.
    2. **Chronological Message Cards:** Collapsible timeline cards with timestamp offsets (`+0ms`, `+38ms`), protocol badges, and summaries.
  - **Deep Packet Inspector:**
    - **Raw Wire Format:** Exact ASCII/text wire format with CRLF line boundaries and real header syntax.
    - **Decoded Fields Table:** Key-value breakdown of status codes, methods, record types, TTLs, and flags.
    - **RFC Protocol Notes:** RFC standard explanations (RFC 1035, RFC 7230, RFC 5321, RFC 8216).

---

## 🚀 Quick Start Instructions

### Prerequisites
- Python 3.8+ (Tested on Python 3.13)
- `Flask` (already installed in your environment)

### Launching the Dashboard

#### Option A: One-Click Launcher (Windows)
Double-click `run.bat` in the project root folder.

#### Option B: Terminal Command
Open PowerShell or Command Prompt in the project folder and run:
```powershell
python app.py
```

Then open your browser and navigate to:
```
http://127.0.0.1:5000
```

---

## 🧪 Running Automated Tests
Run the test suite verifying protocol engine RFC compliance and API routes:
```powershell
python test_engine.py
```
Expected output:
```
....
----------------------------------------------------------------------
Ran 4 tests in 0.118s

OK
```

---

## 📁 Repository Structure

```
dual_panel_protocol_visualizer/
│
├── app.py                     # Flask web server & REST API routes
├── protocol_engine.py         # RFC-compliant protocol simulation engine (DNS, HTTP, SMTP, HLS)
├── test_engine.py             # Automated unit test suite
├── run.bat                    # One-click Windows launch script
├── README.md                  # Project overview & running instructions
│
├── templates/
│   └── index.html             # Dual-panel dashboard layout
│
├── static/
│   ├── style.css              # Cyber-industrial theme, ladder diagram & inspector styling
│   └── app.js                 # State manager, live synchronizer, canvas simulator & controls
│
└── docs/
    ├── REFLECTION.md          # 2-page academic reflection covering AI, synchronization & protocols
    └── AI_USAGE_LOG.md        # Comprehensive AI prompt history and agentic audit trail
```

---

## 🎥 Demo Video Guide (2–4 Minutes)
For your submission video or screenshots:
1. **Introduction (30s):** Show header showing "Google Antigravity · Gemini 3.8 Flash" and dual-panel layout.
2. **Browsing Demo (45s):** Click a preset URL -> click "Visit Page" -> watch DNS query/answer arrow -> TCP handshake -> HTTP GET -> 200 OK -> observe left viewport render the HTML. Click on the HTTP Response card and inspect the Raw Wire Format.
3. **Mail Demo (45s):** Switch to Mail tab -> click "Send Email" -> watch DNS MX query -> SMTP EHLO -> 250 multiline extensions -> MAIL FROM -> RCPT TO -> DATA -> 250 Queued -> observe sent receipt appear on left panel.
4. **Streaming Demo (45s):** Switch to Streaming tab -> click "Play" -> watch HLS Master Manifest fetch -> Variant playlist fetch -> consecutive segment chunks download -> watch buffer bar fill to 16s and animated video pattern run. Change quality to 1080p and watch adaptive re-negotiation.
5. **Playback Controls Demo (15s):** Use Prev/Next step buttons, pause, and adjust speed to 2.0x.
