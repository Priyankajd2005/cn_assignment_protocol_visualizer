# AI Usage Log & Agentic Audit Trail

**Course:** Computer Networks – Application Layer  
**Assignment:** Dual-Panel Activity & Protocol Visualizer  
**Agentic Platform:** Google Antigravity  
**Underlying Model:** Gemini 3.8 Flash (High Reasoning)  
**Execution Environment:** Windows 11 / Python 3.13 / Flask 3.1.3  

---

## 1. Summary of AI Agent Assistance

The entire lifecycle of this project was conducted with substantial assistance from the **Google Antigravity** agentic AI development platform:

1. **Architecture & Requirements Planning:** The agent analyzed the 3-page assignment specification PDF, cataloged all mandatory constraints (exact dual-panel layout, Browsing/Mail/Streaming activities, step-by-step playback controls, packet wire inspection, synchronization), and produced a comprehensive technical implementation plan (`implementation_plan.md`).
2. **Backend Protocol Engineering:** The agent authored `protocol_engine.py`, implementing deterministic, RFC-accurate message generators for DNS recursive lookups, TCP three-way handshakes, HTTP/1.1 requests/responses, multi-turn RFC 5321 ESMTP conversations, and RFC 8216 HLS media playlists.
3. **Frontend UI/UX Generation:** The agent designed a cyber-industrial responsive interface featuring custom CSS Grid/Flexbox layouts, an animated Sequence Ladder Diagram with dynamic SVG message arrows, a chronological packet card stream, an interactive HTML5 video canvas pattern simulator, and a deep packet inspector.
4. **Automated Testing & Verification:** The agent implemented `test_engine.py`, executing automated unit tests verifying protocol payload structures, status codes, and Flask REST endpoints.
5. **Academic Documentation:** The agent co-authored the 2-page academic reflection (`REFLECTION.md`) analyzing platform rationale, synchronization architecture, AI error corrections, and protocol comparisons.

---

## 2. Prompt History & Iterative Milestones

### Milestone 1: Requirement Ingestion & Architecture Planning
- **User Prompt:** `"give me the folderrr containing all the code of the assignment"`
- **Agent Analysis:** 
  - Inspected local environment (`Python 3.13.15`, `Flask 3.1.3`, `uvicorn`, `requests`).
  - Extracted requirements from assignment PDF: Dual-panel layout, Browsing (DNS->HTTP), Mail (DNS->SMTP), Streaming (DNS->HLS), pause/step/replay controls, deep inspection.
  - Created `implementation_plan.md` artifact outlining directory structure, REST APIs, state manager, and testing plan.

### Milestone 2: Backend Protocol Simulator & Unit Testing
- **Agent Action:** 
  - Generated `protocol_engine.py` with classes for `ProtocolStep` and `ProtocolEngine`.
  - Implemented `app.py` providing REST endpoints (`/api/protocols/browse`, `/api/protocols/mail`, `/api/protocols/stream`, `/api/health`).
  - Built and executed `test_engine.py` (4 automated tests covering DNS, HTTP, SMTP, HLS, and Flask endpoints: 100% pass rate in 0.118s).

### Milestone 3: Interactive Dual-Panel UI & Live Synchronization
- **Agent Action:**
  - Generated `templates/index.html` featuring side-by-side activity and visualizer panels.
  - Implemented `static/style.css` with responsive layout, protocol color schemes, and dark theme.
  - Authored `static/app.js` featuring `VisualizerApp` class managing step-by-step playback, auto-animation, speed switching, sequence ladder rendering, and live synchronization hooks with the left panel.

### Milestone 4: Deliverables & Reflection Synthesis
- **Agent Action:**
  - Created `docs/REFLECTION.md` fulfilling all 4 rubric reflection requirements.
  - Created `README.md` with installation, running instructions, and demo video script.
  - Built `run.bat` for one-click startup.

---

## 3. Tool Invocations & Artifact Verification Log
- `write_to_file`: Created `implementation_plan.md`, `builder_part1.py`, `builder_part2.py`, `builder_css.py`, `builder_js.py`, `builder_clean_docs.py`.
- `run_command`: Ran PowerShell directory initializations, python builder scripts, and `python test_engine.py` (Ran 4 tests in 0.118s, OK).
- Model verified: Gemini 3.8 Flash (High Reasoning).
