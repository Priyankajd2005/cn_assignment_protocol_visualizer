# Application + Transport Layer Visualizer (Assignment 2)

Extends the Assignment 1 dashboard so the right panel supports **two synchronized views** of the same exchange: an Application-layer view (DNS/HTTP/SMTP/HLS) and a Transport-layer view focused on TCP communication, including connection establishment, data transfer, and connection termination. Both views are driven by the same underlying step timeline so the protocol information and playback remain synchronized.

## Application + Transport Layer Visualization

The Application + Transport Layer Visualizer is an educational Computer Networks project that demonstrates how Application Layer protocols and Transport Layer communication work together.

The project provides interactive visualization of protocols such as DNS, HTTP, SMTP, and HLS at the Application Layer.

The Transport Layer visualization demonstrates TCP communication through connection establishment, data communication, and connection termination.

Users can inspect important TCP information such as **Sequence Number, Acknowledgement Number, TCP Flags, Window Size, MSS, and TCP State**.

The project provides step-by-step protocol visualization, structured packet information, and playback controls to help students understand how network communication takes place between a client and a server.

The application is built using a Flask backend and a JavaScript-based frontend, combining protocol simulation logic with an interactive Computer Networks dashboard.

## 🆕 What's New in Assignment 2

- **Transport Layer View** — A dedicated Transport Layer visualization has been added to the existing Application Layer protocol visualizer.

- **TCP Handshake** — The project now visualizes TCP connection establishment using SYN, SYN-ACK, and ACK segments.

- **TCP Data Communication** — TCP data-transfer steps are represented with important fields such as Sequence Number, Acknowledgement Number, TCP Flags, Window Size, and MSS.

- **TCP Connection Termination** — The project visualizes TCP connection termination using FIN and ACK communication and shows the final TCP state.

- **TCP State Tracking** — TCP state information is displayed during the simulation to help users understand the lifecycle of a TCP connection.

- **Configurable Ports** — Source and destination port numbers can be provided for Transport Layer simulations.

- **Transport Packet Inspector** — Each Transport Layer step provides detailed information including direction, summary, timing, TCP flags, sequence number, acknowledgement number, window size, MSS, and TCP state.

- **Step-by-Step Playback** — Users can explore the TCP communication sequence using playback controls such as previous, next, pause, replay, and speed controls.

- **Dedicated Transport API** — A dedicated `/api/protocols/transport` endpoint has been added for generating Transport Layer simulation data.

- **Application + Transport Integration** — Assignment 2 connects Application Layer protocol concepts with Transport Layer TCP communication in one interactive visualization.

## 🔢 How Seq/Ack Tracking Works

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

Example TCP flow:

Client                         Server

SYN
Seq = X
        -------------------->

                         SYN-ACK
                         Seq = Y
                         Ack = X + 1
        <--------------------

ACK
Seq = X + 1
Ack = Y + 1
        -------------------->

This provides a visual representation of the sequence and acknowledgement mechanism used by TCP.

## 🔄 How the Two Views Stay Synchronized

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

When the user starts an activity:

1. The frontend sends a request to the Flask backend.
2. The backend runs the corresponding protocol simulation.
3. The simulation engine generates an ordered list of protocol steps.
4. The steps are returned as JSON.
5. JavaScript stores the steps in the current simulation state.
6. The visualization panel renders the selected step.
7. Playback controls move through the same ordered sequence.

For Transport Layer simulation, the frontend uses the dedicated:

`/api/protocols/transport`

endpoint.

This keeps the protocol information and visual playback synchronized with the selected simulation.

## 📁 Project Structure

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

 Backend

- `app.py` — Flask application and REST API routes
- `protocol_engine.py` — Application and Transport Layer simulation logic
- `test_engine.py` — Automated tests
- `requirements.txt` — Project dependencies

 Frontend

- `templates/index.html` — Main dashboard structure
- `static/app.js` — Simulation state, API communication, playback and visualization logic
- `static/style.css` — Dashboard layout and styling

What's Simulated vs. Real

This project is an **educational protocol visualizer**. The network communication shown in the dashboard is simulated rather than generated through real network connections.

 Simulated

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
- TCP state information

 Real

The following parts are real software components:

- Flask web server
- REST API requests
- JavaScript frontend
- Browser rendering
- User input handling
- Playback controls
- JSON data exchange between frontend and backend
- Python protocol simulation engine
- Automated Python tests

The project does not open real TCP connections to external servers for the protocol visualization. Instead, it generates structured protocol events for educational demonstration.

 Assignment 2 Learning Objectives

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

Students can understand:

- Application Layer protocols
- Transport Layer responsibilities
- TCP connection establishment
- TCP data communication
- TCP connection termination
- Sequence and acknowledgement numbers
- TCP flags
- TCP states
- Source and destination ports
- Protocol communication flow

 Extra Credit Ideas

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

 Project Summary

The **Application + Transport Layer Visualizer** combines Application Layer protocol simulations with Transport Layer TCP visualization in a single interactive dashboard.

The project focuses on making networking concepts easier to understand by showing protocol messages, packet fields, TCP states, sequence numbers, acknowledgements, and communication timelines step by step.

It is designed as an educational simulation and does not replace real packet-capture tools or real network traffic analysis.

 👥 Contributors

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
