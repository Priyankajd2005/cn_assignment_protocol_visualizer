"""
Dual-Panel Activity & Protocol Visualizer Web Application
Fast, responsive Flask backend serving REST API endpoints and web UI.
"""

from flask import Flask, render_template, request, jsonify
from protocol_engine import ProtocolEngine

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/protocols/browse", methods=["GET", "POST"])
def browse_protocol():
    data = request.get_json(silent=True) or request.args
    url = data.get("url", "https://example.com/index.html")
    enable_tcp = str(data.get("tcp", "true")).lower() in ["true", "1", "yes"]
    result = ProtocolEngine.simulate_browsing(url=url, enable_tcp_handshake=enable_tcp)
    return jsonify(result)

@app.route("/api/protocols/mail", methods=["GET", "POST"])
def mail_protocol():
    data = request.get_json(silent=True) or request.args
    to_addr = data.get("to", "alice@networks-lab.edu")
    subject = data.get("subject", "Application Layer Project Demo")
    body = data.get("body", "Hello from the Dual-Panel Protocol Visualizer!\r\nSMTP exchange confirmed.")
    from_addr = data.get("from", "student@antigravity-agent.org")
    result = ProtocolEngine.simulate_mail(to_addr=to_addr, subject=subject, body=body, from_addr=from_addr)
    return jsonify(result)

@app.route("/api/protocols/stream", methods=["GET", "POST"])
def stream_protocol():
    data = request.get_json(silent=True) or request.args
    quality = data.get("quality", "720p")
    segments = int(data.get("segments", 4))
    result = ProtocolEngine.simulate_streaming(quality=quality, segment_count=segments)
    return jsonify(result)

@app.route("/api/health")
def health():
    return jsonify({
        "status": "healthy",
        "service": "Dual-Panel Protocol Visualizer",
        "model": "Google Antigravity / Gemini 3.8 Flash",
        "protocols": ["DNS", "HTTP", "SMTP", "HLS"]
    })

if __name__ == "__main__":
    print("==================================================================")
    print(" Dual-Panel Activity & Protocol Visualizer is starting...")
    print(" Open in your browser: http://127.0.0.1:5000")
    print("==================================================================")
    app.run(host="127.0.0.1", port=5000, debug=True)
