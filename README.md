 # Application + Transport Layer Visualizer (Assignment 2)

# Application + Transport Layer Visualization 

The **Application + Transport Layer Visualizer** is an educational Computer Networks project that demonstrates how Application Layer activities interact with Transport Layer communication.

The project provides an interactive dashboard where users can visualize:   

- Browsing
- Mail
- Streaming
- DNS
- HTTP
- SMTP
- HLS
- TCP communication
- TCP handshake
- TCP connection termination
- TCP packet fields
- Sequence and acknowledgement information

The interface provides step-by-step protocol visualization with playback controls, packet information, raw wire representation, decoded fields and TCP state information.

---

 # What's New in Assignment 2

Assignment 2 extends the original Application Layer visualizer by adding Transport Layer functionality.

 Major additions:

- Dedicated Transport Layer simulation
- TCP handshake visualization
- TCP connection termination visualization
- Configurable source and destination ports
- TCP sequence numbers
- TCP acknowledgement numbers
- TCP flags
- TCP window information
- MSS information
- TCP state tracking
- Transport Layer packet inspection
- Transport-specific simulation API
- Step-by-step TCP playback
- Application + Transport Layer project integration

The main Transport Layer endpoint is:

    POST /api/protocols/transport

---

# How Seq/Ack Tracking Works

The Transport Layer simulation represents TCP sequence and acknowledgement information for each communication step.

For every TCP segment, the protocol engine generates important TCP fields such as:

- Sequence Number
- Acknowledgement Number
- TCP Flags
- Window Size
- MSS
- TCP State

The generated values are passed from the Flask backend to the frontend as structured simulation data.

The frontend then displays these values in the **Transport Layer packet inspector**, allowing the user to observe how TCP communication changes from connection establishment to data transfer and connection termination.

  # Setup & Run

 1. Clone the repository

    git clone https://github.com/Priyankajd2005/cn_assignment_protocol_visualizer.git

2. Open the project folder

    cd CN_Protocol_Visualizer

 3. Install dependencies

    pip install -r requirements.txt

 4. Run the Flask application

    python app.py

The application will start at:

    http://127.0.0.1:5000

Open the URL in your browser to use the Application + Transport Layer Visualizer.

 Live Demo

[Open Live Project](https://cn-assignment-protocol-visualizer-2.onrender.com)

---

# How the Two Views Stay Synchronized

The project uses a common simulation-step structure between the activity and protocol visualization panels.

The synchronization flow is:

    User Action
        ↓
    Flask Backend
        ↓
    Protocol Simulation Engine
        ↓
    Protocol Steps
        ↓
    JavaScript State Manager
        ↓
    Right-Side Protocol Visualization

 # When the user starts an activity:

1. The frontend sends a request to the Flask backend.
2. The backend runs the corresponding protocol simulation.
3. The simulation engine generates an ordered list of protocol steps.
4. The steps are returned as JSON.
5. JavaScript stores the steps in the current simulation state.
6. The visualization panel renders the selected step.
7. Playback controls move through the same ordered sequence.

For Transport Layer simulation, the frontend uses the dedicated:

    /api/protocols/transport

endpoint.

This keeps the protocol information and visual playback synchronized with the selected simulation.

---

# 📁 Project Structure

    CN_Protocol_Visualizer/
    │
    ├── app.py
    ├── protocol_engine.py
    ├── test_engine.py
    ├── requirements.txt
    ├── README.md
    │
    ├── templates/
    │   └── index.html
    │
    └── static/
        ├── app.js
        └── style.css

# Backend

- `app.py` — Flask application and REST API routes
- `protocol_engine.py` — Application and Transport Layer simulation logic
- `test_engine.py` — Automated tests
- `requirements.txt` — Project dependencies

# Frontend

- `templates/index.html` — Main dashboard structure
- `static/app.js` — Simulation state, API communication, playback and visualization logic
- `static/style.css` — Dashboard layout and styling

---

 What's Simulated vs. Real

This project is an **educational protocol visualizer**. The network communication shown in the dashboard is simulated rather than generated through real network connections.

# Simulated

- DNS resolution
- HTTP request/response
- SMTP communication
- HLS streaming
- TCP handshake
- TCP data communication
- TCP connection termination
- TCP packet fields
- Sequence and acknowledgement values
- Protocol timing
- Packet/wire representation

# Real

The following parts are real software components:

- Flask web server
- REST API requests
- JavaScript frontend
- Browser rendering
- User input handling
- Playback controls
- JSON data exchange between frontend and backend
- Automated Python tests

The project does not open real TCP connections to external servers for the protocol visualization. Instead, it generates realistic protocol events for educational demonstration.

---

 # Assignment 2 Learning Objectives

The project demonstrates how Application Layer activities interact with Transport Layer communication.

Students can observe:

    Application Layer
           ↓
    DNS / HTTP / SMTP / HLS
           ↓
    Transport Layer
           ↓
    TCP
           ↓
    TCP Segments
           ↓
    Client ↔ Server Communication

This makes it easier to connect theoretical Computer Networks concepts with an interactive visual representation.

---

# Extra Credit Ideas

The current project uses simulated network traffic. Possible future extensions include:

1. Real TCP Communication

Connect the visualizer to a real TCP client/server implementation instead of simulated TCP events.

 2. Congestion Window Visualization

Add a graphical representation of TCP congestion control, including:

- Slow Start
- Congestion Avoidance
- Congestion Window
- Retransmission events
 3. Persistent vs Non-Persistent HTTP

Add a comparison between:

- HTTP persistent connections
- HTTP non-persistent connections

 4. Packet Loss Simulation

Allow users to introduce packet loss and visualize TCP retransmission and acknowledgement behavior.

 5. UDP Transport Visualization

Add UDP alongside TCP and compare:

    TCP                         UDP
    │                           │
    Connection-oriented         Connectionless
    Reliable                    No delivery guarantee
    Sequence/Ack                No Sequence/Ack
    Flow control                No TCP-style flow control

 6. QUIC / HTTP/3

A future version could visualize QUIC and HTTP/3 communication and compare it with traditional TCP + HTTP.

---

# Project Summary

The **Application + Transport Layer Visualizer** combines Application Layer protocol simulations with Transport Layer TCP visualization in a single interactive dashboard.

The project focuses on making networking concepts easier to understand by showing protocol messages, packet fields, TCP states, sequence numbers, acknowledgements, and communication timelines step by step.

It is designed as an educational simulation and does not replace real packet-capture tools or real network traffic analysis.

---

# Contributors

This project was developed as part of the Computer Networks Assignment 2.

<a href="https://github.com/Priyankajd2005">
  <img src="https://github.com/Priyankajd2005.png" width="80" alt="Priyanka Jd">
</a>

Priyanka Jd

Development, protocol visualization, Transport Layer integration and testing.

[GitHub Profile](https://github.com/Priyankajd2005)

 Project Collaboration

Application Layer and Transport Layer visualization development.

[View All Contributors](https://github.com/Priyankajd2005/cn_assignment_protocol_visualizer/graphs/contributors)

# Languages

- Python
- JavaScript
- HTML
- CSS

 # Technologies & Frameworks

- Flask
- REST API
- JSON
- Git & GitHub
- Gunicorn
