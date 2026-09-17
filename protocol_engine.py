"""
Protocol Engine for Dual-Panel Activity & Protocol Visualizer
Simulates realistic Application Layer protocol exchanges:
- DNS (RFC 1035): Recursive resolution, A/AAAA/MX queries & answers
- HTTP (RFC 7230/7231): GET requests, status codes, headers, body formatting
- SMTP (RFC 5321): Complete mail transfer handshake (EHLO, MAIL FROM, RCPT TO, DATA, QUIT)
- HLS Streaming (RFC 8216): Master playlist, media playlist, and chunked transport segments
"""

import time
import hashlib
from datetime import datetime, timezone
from urllib.parse import urlparse

def get_simulated_ip(domain: str) -> str:
    """Generate a consistent realistic public IP address for a domain."""
    h = hashlib.md5(domain.encode("utf-8")).hexdigest()
    octet2 = (int(h[0:2], 16) % 150) + 50
    octet3 = (int(h[2:4], 16) % 200) + 10
    octet4 = (int(h[4:6], 16) % 250) + 2
    return f"142.{octet2}.{octet3}.{octet4}"

def get_simulated_mx(domain: str) -> str:
    """Generate mail exchanger hostname for a domain."""
    clean_domain = domain.split("@")[-1].strip()
    return f"mx1.mail.{clean_domain}"

class ProtocolStep:
    def __init__(self, step_id: int, protocol: str, title: str,
                 direction: str, sender: str, receiver: str,
                 time_offset_ms: int, summary: str,
                 raw_wire: str, key_fields: dict, category: str = "app"):
        self.step_id = step_id
        self.protocol = protocol          # DNS, TCP, HTTP, SMTP, HLS
        self.title = title
        self.direction = direction        # "client_to_server" | "server_to_client" | "client_to_dns" | "dns_to_client"
        self.sender = sender
        self.receiver = receiver
        self.time_offset_ms = time_offset_ms
        self.summary = summary
        self.raw_wire = raw_wire
        self.key_fields = key_fields
        self.category = category          # "dns" | "handshake" | "http" | "smtp" | "media"

    def to_dict(self):
        return {
            "step_id": self.step_id,
            "protocol": self.protocol,
            "title": self.title,
            "direction": self.direction,
            "sender": self.sender,
            "receiver": self.receiver,
            "time_offset_ms": self.time_offset_ms,
            "summary": self.summary,
            "raw_wire": self.raw_wire,
            "key_fields": self.key_fields,
            "category": self.category
        }

class ProtocolEngine:
    """Orchestrates protocol simulations for Browsing, Mail, and Streaming."""

    @staticmethod
    def simulate_browsing(url: str, enable_tcp_handshake: bool = True) -> dict:
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "https://" + url

        parsed = urlparse(url)
        host = parsed.hostname or "example.com"
        port = parsed.port or (443 if parsed.scheme == "https" else 80)
        path = parsed.path if parsed.path else "/"
        if parsed.query:
            path += f"?{parsed.query}"

        client_ip = "192.168.1.105"
        dns_server = "8.8.8.8"
        server_ip = get_simulated_ip(host)

        steps = []
        step_counter = 1
        elapsed = 0

        # 1. DNS QUERY
        dns_query_raw = (
            f";; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 41829\n"
            f";; flags: rd; QUERY: 1, ANSWER: 0, AUTHORITY: 0, ADDITIONAL: 1\n"
            f";; QUESTION SECTION:\n"
            f";{host}. IN A\n\n"
            f";; EDNS: version: 0, flags:; udp: 4096"
        )
        steps.append(ProtocolStep(
            step_id=step_counter,
            protocol="DNS",
            title=f"DNS Standard Query: {host} (Type A)",
            direction="client_to_dns",
            sender=f"Client ({client_ip}:53421)",
            receiver=f"DNS Resolver ({dns_server}:53)",
            time_offset_ms=elapsed,
            summary=f"Client queries recursive DNS resolver to resolve '{host}' to an IPv4 address.",
            raw_wire=dns_query_raw,
            key_fields={
                "Transaction ID": "0xa365 (41829)",
                "Query Type": "A (Host Address)",
                "Class": "IN (Internet)",
                "Domain": host,
                "Recursion Desired": "True"
            },
            category="dns"
        ))
        step_counter += 1
        elapsed += 38

        # 2. DNS RESPONSE
        dns_resp_raw = (
            f";; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 41829\n"
            f";; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1\n"
            f";; ANSWER SECTION:\n"
            f"{host}.\t300\tIN\tA\t{server_ip}\n\n"
            f";; Query time: 38 msec\n"
            f";; SERVER: {dns_server}#53({dns_server})"
        )
        steps.append(ProtocolStep(
            step_id=step_counter,
            protocol="DNS",
            title=f"DNS Query Response: {host} -> {server_ip}",
            direction="dns_to_client",
            sender=f"DNS Resolver ({dns_server}:53)",
            receiver=f"Client ({client_ip}:53421)",
            time_offset_ms=elapsed,
            summary=f"DNS Resolver returns A record: '{host}' maps to IP {server_ip} (TTL=300s).",
            raw_wire=dns_resp_raw,
            key_fields={
                "Response Code": "NOERROR (0)",
                "Resolved IP": server_ip,
                "TTL": "300 seconds",
                "Authoritative": "No (Cached/Recursive)",
                "Record Count": "1 Answer"
            },
            category="dns"
        ))
        step_counter += 1
        elapsed += 12

        # 3. TCP 3-Way Handshake
        if enable_tcp_handshake:
            steps.append(ProtocolStep(
                step_id=step_counter,
                protocol="TCP",
                title=f"TCP Handshake [SYN]: Client -> Server Port {port}",
                direction="client_to_server",
                sender=f"Client ({client_ip}:49822)",
                receiver=f"Web Server ({server_ip}:{port})",
                time_offset_ms=elapsed,
                summary="Client initiates reliable transport connection by synchronizing sequence numbers.",
                raw_wire=f"TCP Header: SrcPort=49822, DstPort={port}, Seq=0, Ack=0, Flags=[SYN], Win=65535, MSS=1460",
                key_fields={"Flags": "SYN", "Seq": 0, "Ack": 0, "MSS": 1460, "Window": 65535},
                category="handshake"
            ))
            step_counter += 1
            elapsed += 22

            steps.append(ProtocolStep(
                step_id=step_counter,
                protocol="TCP",
                title="TCP Handshake [SYN, ACK]: Server -> Client",
                direction="server_to_client",
                sender=f"Web Server ({server_ip}:{port})",
                receiver=f"Client ({client_ip}:49822)",
                time_offset_ms=elapsed,
                summary="Server acknowledges client's SYN and sends its own sequence synchronization.",
                raw_wire=f"TCP Header: SrcPort={port}, DstPort=49822, Seq=0, Ack=1, Flags=[SYN, ACK], Win=65535, MSS=1460",
                key_fields={"Flags": "SYN, ACK", "Seq": 0, "Ack": 1, "Window": 65535},
                category="handshake"
            ))
            step_counter += 1
            elapsed += 21

            steps.append(ProtocolStep(
                step_id=step_counter,
                protocol="TCP",
                title="TCP Handshake [ACK]: Client -> Server (Connection Established)",
                direction="client_to_server",
                sender=f"Client ({client_ip}:49822)",
                receiver=f"Web Server ({server_ip}:{port})",
                time_offset_ms=elapsed,
                summary="Client acknowledges server's SYN. TCP connection is now ESTABLISHED.",
                raw_wire=f"TCP Header: SrcPort=49822, DstPort={port}, Seq=1, Ack=1, Flags=[ACK], Win=65535",
                key_fields={"Flags": "ACK", "Seq": 1, "Ack": 1, "State": "ESTABLISHED"},
                category="handshake"
            ))
            step_counter += 1
            elapsed += 8

        # 4. HTTP REQUEST
        http_req_raw = (
            f"GET {path} HTTP/1.1\r\n"
            f"Host: {host}\r\n"
            f"User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/128.0.0.0 Safari/537.36\r\n"
            f"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\r\n"
            f"Accept-Language: en-US,en;q=0.9\r\n"
            f"Accept-Encoding: gzip, deflate, br\r\n"
            f"Connection: keep-alive\r\n"
            f"Upgrade-Insecure-Requests: 1\r\n"
            f"Sec-Fetch-Dest: document\r\n"
            f"Sec-Fetch-Mode: navigate\r\n"
            f"Sec-Fetch-Site: none\r\n"
            f"\r\n"
        )
        steps.append(ProtocolStep(
            step_id=step_counter,
            protocol="HTTP",
            title=f"HTTP/1.1 Request: GET {path}",
            direction="client_to_server",
            sender=f"Client ({client_ip})",
            receiver=f"Web Server ({server_ip}:{port})",
            time_offset_ms=elapsed,
            summary=f"Client transmits HTTP GET request asking for resource '{path}' from host {host}.",
            raw_wire=http_req_raw,
            key_fields={
                "Method": "GET",
                "URI": path,
                "Version": "HTTP/1.1",
                "Host Header": host,
                "Connection": "keep-alive"
            },
            category="http"
        ))
        step_counter += 1
        elapsed += 45

        # 5. HTTP RESPONSE
        now_rfc = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S GMT")
        mock_html = (
            f"<!DOCTYPE html>\n"
            f"<html lang=\"en\">\n"
            f"<head>\n"
            f"  <meta charset=\"UTF-8\">\n"
            f"  <title>Welcome to {host}</title>\n"
            f"  <style>\n"
            f"    body {{ font-family: system-ui, sans-serif; padding: 24px; color: #1e293b; background: #f8fafc; }}\n"
            f"    h1 {{ color: #0f172a; margin-bottom: 8px; }}\n"
            f"    .badge {{ display: inline-block; background: #dcfce7; color: #166534; padding: 4px 10px; border-radius: 9999px; font-weight: 600; font-size: 12px; }}\n"
            f"    .card {{ background: white; border: 1px solid #e2e8f0; border-radius: 8px; padding: 16px; margin-top: 16px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }}\n"
            f"  </style>\n"
            f"</head>\n"
            f"<body>\n"
            f"  <div class=\"badge\">HTTP/1.1 200 OK</div>\n"
            f"  <h1>Connected to {host}!</h1>\n"
            f"  <p>Resource requested at path <code>{path}</code> delivered successfully via TCP port {port}.</p>\n"
            f"  <div class=\"card\">\n"
            f"    <p><b>Server IP:</b> {server_ip}</p>\n"
            f"    <p><b>Content-Type:</b> text/html; charset=UTF-8</p>\n"
            f"    <p><b>Caching:</b> max-age=3600, public</p>\n"
            f"  </div>\n"
            f"</body>\n"
            f"</html>"
        )
        content_len = len(mock_html.encode("utf-8"))
        etag = f"\"{hashlib.sha256(mock_html.encode()).hexdigest()[:16]}\""

        http_resp_raw = (
            f"HTTP/1.1 200 OK\r\n"
            f"Date: {now_rfc}\r\n"
            f"Server: Apache/2.4.52 (Ubuntu)\r\n"
            f"Content-Type: text/html; charset=UTF-8\r\n"
            f"Content-Length: {content_len}\r\n"
            f"Connection: keep-alive\r\n"
            f"Cache-Control: max-age=3600, public\r\n"
            f"ETag: {etag}\r\n"
            f"\r\n"
            f"{mock_html}"
        )
        steps.append(ProtocolStep(
            step_id=step_counter,
            protocol="HTTP",
            title="HTTP/1.1 Response: 200 OK",
            direction="server_to_client",
            sender=f"Web Server ({server_ip}:{port})",
            receiver=f"Client ({client_ip})",
            time_offset_ms=elapsed,
            summary=f"Web server delivers 200 OK status line, HTTP response headers, and HTML payload ({content_len} bytes).",
            raw_wire=http_resp_raw,
            key_fields={
                "Status Code": "200 OK",
                "Content-Type": "text/html; charset=UTF-8",
                "Content-Length": f"{content_len} bytes",
                "Cache-Control": "max-age=3600, public",
                "Server Software": "Apache/2.4.52 (Ubuntu)"
            },
            category="http"
        ))

        return {
            "activity": "browsing",
            "url": url,
            "host": host,
            "server_ip": server_ip,
            "port": port,
            "rendered_content": mock_html,
            "total_time_ms": elapsed,
            "steps": [s.to_dict() for s in steps]
        }

    @staticmethod
    def simulate_mail(to_addr: str, subject: str, body: str,
                      from_addr: str = "alice@client-network.edu") -> dict:
        if not to_addr or "@" not in to_addr:
            to_addr = "bob@example.com"
        if not subject:
            subject = "Computer Networks Assignment Demo"
        if not body:
            body = "Hello! This email exchange is visualized via SMTP (RFC 5321)."

        recipient_domain = to_addr.split("@")[-1].strip()
        mx_host = get_simulated_mx(recipient_domain)
        mx_ip = get_simulated_ip(mx_host)
        client_ip = "192.168.1.105"
        dns_server = "8.8.8.8"

        steps = []
        step_counter = 1
        elapsed = 0

        # 1. DNS MX Query
        dns_mx_query = (
            f";; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 18921\n"
            f";; flags: rd; QUERY: 1, ANSWER: 0, AUTHORITY: 0, ADDITIONAL: 0\n"
            f";; QUESTION SECTION:\n"
            f";{recipient_domain}.\tIN\tMX"
        )
        steps.append(ProtocolStep(
            step_id=step_counter,
            protocol="DNS",
            title=f"DNS MX Query: {recipient_domain}",
            direction="client_to_dns",
            sender=f"Client ({client_ip}:48192)",
            receiver=f"DNS Resolver ({dns_server}:53)",
            time_offset_ms=elapsed,
            summary=f"Lookup Mail Exchanger (MX) resource record for recipient domain '{recipient_domain}'.",
            raw_wire=dns_mx_query,
            key_fields={
                "Query Name": recipient_domain,
                "Query Type": "MX (Mail Exchange)",
                "Transaction ID": "0x49e9"
            },
            category="dns"
        ))
        step_counter += 1
        elapsed += 41

        # 2. DNS MX Response
        dns_mx_resp = (
            f";; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 18921\n"
            f";; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1\n"
            f";; ANSWER SECTION:\n"
            f"{recipient_domain}.\t300\tIN\tMX\t10 {mx_host}.\n"
            f";; ADDITIONAL SECTION:\n"
            f"{mx_host}.\t300\tIN\tA\t{mx_ip}"
        )
        steps.append(ProtocolStep(
            step_id=step_counter,
            protocol="DNS",
            title=f"DNS MX Response: {recipient_domain} -> {mx_host} ({mx_ip})",
            direction="dns_to_client",
            sender=f"DNS Resolver ({dns_server}:53)",
            receiver=f"Client ({client_ip}:48192)",
            time_offset_ms=elapsed,
            summary=f"Resolved MX host '{mx_host}' (Preference 10) with IP {mx_ip}.",
            raw_wire=dns_mx_resp,
            key_fields={
                "Preference": 10,
                "MX Host": mx_host,
                "Resolved IP": mx_ip,
                "TTL": "300s"
            },
            category="dns"
        ))
        step_counter += 1
        elapsed += 25

        # 3. Server 220 Service Ready
        smtp_220 = f"220 {mx_host} ESMTP Postfix (Debian/GNU) Service Ready\r\n"
        steps.append(ProtocolStep(
            step_id=step_counter,
            protocol="SMTP",
            title="SMTP Greeting: 220 Service Ready",
            direction="server_to_client",
            sender=f"SMTP Server ({mx_ip}:25)",
            receiver=f"Client ({client_ip}:50124)",
            time_offset_ms=elapsed,
            summary=f"Mail Transfer Agent (MTA) {mx_host} welcomes client on port 25.",
            raw_wire=smtp_220,
            key_fields={
                "Reply Code": "220 (Service Ready)",
                "Host": mx_host,
                "Service": "ESMTP Postfix"
            },
            category="smtp"
        ))
        step_counter += 1
        elapsed += 15

        # 4. Client EHLO
        client_hostname = "mailclient.local"
        smtp_ehlo = f"EHLO {client_hostname}\r\n"
        steps.append(ProtocolStep(
            step_id=step_counter,
            protocol="SMTP",
            title=f"SMTP Greeting: EHLO {client_hostname}",
            direction="client_to_server",
            sender=f"Client ({client_ip}:50124)",
            receiver=f"SMTP Server ({mx_ip}:25)",
            time_offset_ms=elapsed,
            summary="Client introduces itself with Extended HELLO (EHLO).",
            raw_wire=smtp_ehlo,
            key_fields={
                "Command": "EHLO",
                "Client Host": client_hostname
            },
            category="smtp"
        ))
        step_counter += 1
        elapsed += 20

        # 5. Server 250 Multiline Extensions
        smtp_250_ehlo = (
            f"250-{mx_host} Hello {client_hostname} [{client_ip}]\r\n"
            f"250-SIZE 35882577\r\n"
            f"250-8BITMIME\r\n"
            f"250-PIPELINING\r\n"
            f"250-STARTTLS\r\n"
            f"250 HELP\r\n"
        )
        steps.append(ProtocolStep(
            step_id=step_counter,
            protocol="SMTP",
            title="SMTP Capabilities: 250 Multi-Line Response",
            direction="server_to_client",
            sender=f"SMTP Server ({mx_ip}:25)",
            receiver=f"Client ({client_ip}:50124)",
            time_offset_ms=elapsed,
            summary="Server lists supported ESMTP extensions (SIZE, 8BITMIME, STARTTLS).",
            raw_wire=smtp_250_ehlo,
            key_fields={
                "Reply Code": "250 (OK / Capabilities)",
                "Max Size": "35,882,577 bytes",
                "Extensions": "8BITMIME, PIPELINING, STARTTLS"
            },
            category="smtp"
        ))
        step_counter += 1
        elapsed += 18

        # 6. Client MAIL FROM
        smtp_mail_from = f"MAIL FROM:<{from_addr}>\r\n"
        steps.append(ProtocolStep(
            step_id=step_counter,
            protocol="SMTP",
            title=f"SMTP Sender: MAIL FROM:<{from_addr}>",
            direction="client_to_server",
            sender=f"Client ({client_ip}:50124)",
            receiver=f"SMTP Server ({mx_ip}:25)",
            time_offset_ms=elapsed,
            summary=f"Initiate mail transaction envelope with reverse path <{from_addr}>.",
            raw_wire=smtp_mail_from,
            key_fields={
                "Command": "MAIL FROM",
                "Reverse Path": f"<{from_addr}>"
            },
            category="smtp"
        ))
        step_counter += 1
        elapsed += 22

        # 7. Server 250 Sender OK
        smtp_250_sender = f"250 2.1.0 Ok: Sender <{from_addr}> accepted\r\n"
        steps.append(ProtocolStep(
            step_id=step_counter,
            protocol="SMTP",
            title="SMTP Status: 250 Sender OK",
            direction="server_to_client",
            sender=f"SMTP Server ({mx_ip}:25)",
            receiver=f"Client ({client_ip}:50124)",
            time_offset_ms=elapsed,
            summary=f"Server confirms sender address <{from_addr}> is valid and accepted.",
            raw_wire=smtp_250_sender,
            key_fields={
                "Reply Code": "250 (Sender Accepted)",
                "Status": "2.1.0 Ok"
            },
            category="smtp"
        ))
        step_counter += 1
        elapsed += 15

        # 8. Client RCPT TO
        smtp_rcpt_to = f"RCPT TO:<{to_addr}>\r\n"
        steps.append(ProtocolStep(
            step_id=step_counter,
            protocol="SMTP",
            title=f"SMTP Recipient: RCPT TO:<{to_addr}>",
            direction="client_to_server",
            sender=f"Client ({client_ip}:50124)",
            receiver=f"SMTP Server ({mx_ip}:25)",
            time_offset_ms=elapsed,
            summary=f"Specify destination recipient <{to_addr}>.",
            raw_wire=smtp_rcpt_to,
            key_fields={
                "Command": "RCPT TO",
                "Forward Path": f"<{to_addr}>"
            },
            category="smtp"
        ))
        step_counter += 1
        elapsed += 24

        # 9. Server 250 Recipient OK
        smtp_250_rcpt = f"250 2.1.5 Ok: Recipient <{to_addr}> accepted\r\n"
        steps.append(ProtocolStep(
            step_id=step_counter,
            protocol="SMTP",
            title="SMTP Status: 250 Recipient OK",
            direction="server_to_client",
            sender=f"SMTP Server ({mx_ip}:25)",
            receiver=f"Client ({client_ip}:50124)",
            time_offset_ms=elapsed,
            summary=f"Server confirms recipient mailbox exists and is deliverable.",
            raw_wire=smtp_250_rcpt,
            key_fields={
                "Reply Code": "250 (Recipient Accepted)",
                "Status": "2.1.5 Ok"
            },
            category="smtp"
        ))
        step_counter += 1
        elapsed += 16

        # 10. Client DATA
        smtp_data_cmd = "DATA\r\n"
        steps.append(ProtocolStep(
            step_id=step_counter,
            protocol="SMTP",
            title="SMTP Command: DATA",
            direction="client_to_server",
            sender=f"Client ({client_ip}:50124)",
            receiver=f"SMTP Server ({mx_ip}:25)",
            time_offset_ms=elapsed,
            summary="Client requests permission to transmit message payload.",
            raw_wire=smtp_data_cmd,
            key_fields={"Command": "DATA"},
            category="smtp"
        ))
        step_counter += 1
        elapsed += 19

        # 11. Server 354 Start Mail Input
        smtp_354 = "354 End data with <CR><LF>.<CR><LF>\r\n"
        steps.append(ProtocolStep(
            step_id=step_counter,
            protocol="SMTP",
            title="SMTP Intermediate: 354 Start Mail Input",
            direction="server_to_client",
            sender=f"SMTP Server ({mx_ip}:25)",
            receiver=f"Client ({client_ip}:50124)",
            time_offset_ms=elapsed,
            summary="Server instructs client to begin mail content and terminate with single dot.",
            raw_wire=smtp_354,
            key_fields={
                "Reply Code": "354 (Start Mail Input)",
                "Delimiter": "<CRLF>.<CRLF>"
            },
            category="smtp"
        ))
        step_counter += 1
        elapsed += 22

        # 12. Client Message Content & Termination
        now_rfc2822 = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S +0000")
        msg_id = f"<{int(time.time())}.visualizer@{client_hostname}>"
        mail_payload = (
            f"From: {from_addr}\r\n"
            f"To: {to_addr}\r\n"
            f"Date: {now_rfc2822}\r\n"
            f"Subject: {subject}\r\n"
            f"Message-ID: {msg_id}\r\n"
            f"MIME-Version: 1.0\r\n"
            f"Content-Type: text/plain; charset=UTF-8\r\n"
            f"\r\n"
            f"{body}\r\n"
            f".\r\n"
        )
        steps.append(ProtocolStep(
            step_id=step_counter,
            protocol="SMTP",
            title="SMTP Data Payload: RFC 5322 Headers, Body & Trailing '.'",
            direction="client_to_server",
            sender=f"Client ({client_ip}:50124)",
            receiver=f"SMTP Server ({mx_ip}:25)",
            time_offset_ms=elapsed,
            summary="Transmit complete RFC 5322 message stream followed by standard termination marker.",
            raw_wire=mail_payload,
            key_fields={
                "Subject": subject,
                "Message-ID": msg_id,
                "Payload Bytes": len(mail_payload),
                "Termination Sequence": "<CRLF>.<CRLF>"
            },
            category="smtp"
        ))
        step_counter += 1
        elapsed += 35

        # 13. Server 250 Message Queued
        queue_id = f"4X{hashlib.md5(mail_payload.encode()).hexdigest()[:8].upper()}"
        smtp_250_queued = f"250 2.0.0 Ok: queued as {queue_id}\r\n"
        steps.append(ProtocolStep(
            step_id=step_counter,
            protocol="SMTP",
            title=f"SMTP Confirmation: 250 Queued ({queue_id})",
            direction="server_to_client",
            sender=f"SMTP Server ({mx_ip}:25)",
            receiver=f"Client ({client_ip}:50124)",
            time_offset_ms=elapsed,
            summary=f"Message accepted into spool queue for delivery with ID {queue_id}.",
            raw_wire=smtp_250_queued,
            key_fields={
                "Reply Code": "250 (Delivery Accepted)",
                "Queue ID": queue_id,
                "Status": "2.0.0 Ok"
            },
            category="smtp"
        ))
        step_counter += 1
        elapsed += 20

        # 14. Client QUIT
        smtp_quit = "QUIT\r\n"
        steps.append(ProtocolStep(
            step_id=step_counter,
            protocol="SMTP",
            title="SMTP Command: QUIT",
            direction="client_to_server",
            sender=f"Client ({client_ip}:50124)",
            receiver=f"SMTP Server ({mx_ip}:25)",
            time_offset_ms=elapsed,
            summary="Client requests clean closure of SMTP session.",
            raw_wire=smtp_quit,
            key_fields={"Command": "QUIT"},
            category="smtp"
        ))
        step_counter += 1
        elapsed += 14

        # 15. Server 221 Bye
        smtp_221 = f"221 2.0.0 {mx_host} Service closing transmission channel\r\n"
        steps.append(ProtocolStep(
            step_id=step_counter,
            protocol="SMTP",
            title="SMTP Farewell: 221 Channel Closed",
            direction="server_to_client",
            sender=f"SMTP Server ({mx_ip}:25)",
            receiver=f"Client ({client_ip}:50124)",
            time_offset_ms=elapsed,
            summary="Server acknowledges QUIT and terminates TCP transmission channel.",
            raw_wire=smtp_221,
            key_fields={
                "Reply Code": "221 (Service Closing)",
                "Status": "2.0.0 Bye"
            },
            category="smtp"
        ))

        return {
            "activity": "mail",
            "to": to_addr,
            "from": from_addr,
            "subject": subject,
            "body": body,
            "mx_host": mx_host,
            "mx_ip": mx_ip,
            "queue_id": queue_id,
            "total_time_ms": elapsed,
            "steps": [s.to_dict() for s in steps]
        }

    @staticmethod
    def simulate_streaming(quality: str = "720p", segment_count: int = 4) -> dict:
        valid_qualities = {
            "1080p": {"bandwidth": 5200000, "res": "1920x1080", "chunk_kb": 2600},
            "720p":  {"bandwidth": 2800000, "res": "1280x720",  "chunk_kb": 1400},
            "480p":  {"bandwidth": 1200000, "res": "854x480",   "chunk_kb": 600},
            "360p":  {"bandwidth": 600000,  "res": "640x360",   "chunk_kb": 300}
        }
        if quality not in valid_qualities:
            quality = "720p"

        info = valid_qualities[quality]
        cdn_host = "edge-cdn.streampulse.net"
        cdn_ip = "104.22.41.98"
        client_ip = "192.168.1.105"
        dns_server = "8.8.8.8"

        steps = []
        step_counter = 1
        elapsed = 0

        # 1. DNS Query
        dns_query = (
            f";; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 53102\n"
            f";; flags: rd; QUESTION: 1, ANSWER: 0\n"
            f";; QUESTION SECTION:\n"
            f";{cdn_host}.\tIN\tA"
        )
        steps.append(ProtocolStep(
            step_id=step_counter,
            protocol="DNS",
            title=f"DNS Query: CDN Edge {cdn_host}",
            direction="client_to_dns",
            sender=f"Client ({client_ip}:58110)",
            receiver=f"DNS Resolver ({dns_server}:53)",
            time_offset_ms=elapsed,
            summary="Lookup closest CDN Edge server for streaming content.",
            raw_wire=dns_query,
            key_fields={"Domain": cdn_host, "Type": "A"},
            category="dns"
        ))
        step_counter += 1
        elapsed += 32

        # 2. DNS Response
        dns_resp = (
            f";; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 53102\n"
            f";; flags: qr rd ra; ANSWER: 1\n"
            f"{cdn_host}.\t60\tIN\tA\t{cdn_ip}"
        )
        steps.append(ProtocolStep(
            step_id=step_counter,
            protocol="DNS",
            title=f"DNS Response: {cdn_host} -> {cdn_ip}",
            direction="dns_to_client",
            sender=f"DNS Resolver ({dns_server}:53)",
            receiver=f"Client ({client_ip}:58110)",
            time_offset_ms=elapsed,
            summary=f"Discovered nearest low-latency CDN IP {cdn_ip} (TTL=60s).",
            raw_wire=dns_resp,
            key_fields={"Resolved IP": cdn_ip, "TTL": "60s (Dynamic CDN Route)"},
            category="dns"
        ))
        step_counter += 1
        elapsed += 18

        # 3. HTTP GET Master Playlist
        master_url = "/live/hls/master.m3u8"
        req_master = (
            f"GET {master_url} HTTP/1.1\r\n"
            f"Host: {cdn_host}\r\n"
            f"User-Agent: VideoPlayer/2.4 (HLS-Client; Windows x64)\r\n"
            f"Accept: application/vnd.apple.mpegurl, application/x-mpegURL, */*\r\n"
            f"Connection: keep-alive\r\n\r\n"
        )
        steps.append(ProtocolStep(
            step_id=step_counter,
            protocol="HTTP",
            title=f"HLS Fetch: GET Master Playlist ({master_url})",
            direction="client_to_server",
            sender=f"Client ({client_ip})",
            receiver=f"CDN Edge ({cdn_ip}:443)",
            time_offset_ms=elapsed,
            summary="Client requests master manifest describing available bitrates & resolutions.",
            raw_wire=req_master,
            key_fields={
                "Method": "GET",
                "URI": master_url,
                "Accept": "application/vnd.apple.mpegurl"
            },
            category="media"
        ))
        step_counter += 1
        elapsed += 42

        # 4. HTTP 200 Response Master Playlist
        master_body = (
            "#EXTM3U\n"
            "#EXT-X-VERSION:3\n"
            "#EXT-X-INDEPENDENT-SEGMENTS\n"
            "#EXT-X-STREAM-INF:BANDWIDTH=5200000,RESOLUTION=1920x1080,FRAME-RATE=60.000,CODECS=\"avc1.64002a,mp4a.40.2\"\n"
            "1080p/index.m3u8\n"
            "#EXT-X-STREAM-INF:BANDWIDTH=2800000,RESOLUTION=1280x720,FRAME-RATE=30.000,CODECS=\"avc1.4d401f,mp4a.40.2\"\n"
            "720p/index.m3u8\n"
            "#EXT-X-STREAM-INF:BANDWIDTH=1200000,RESOLUTION=854x480,FRAME-RATE=30.000,CODECS=\"avc1.4d401e,mp4a.40.2\"\n"
            "480p/index.m3u8\n"
            "#EXT-X-STREAM-INF:BANDWIDTH=600000,RESOLUTION=640x360,FRAME-RATE=30.000,CODECS=\"avc1.4d4015,mp4a.40.2\"\n"
            "360p/index.m3u8\n"
        )
        resp_master = (
            f"HTTP/1.1 200 OK\r\n"
            f"Content-Type: application/vnd.apple.mpegurl\r\n"
            f"Content-Length: {len(master_body.encode())}\r\n"
            f"Cache-Control: max-age=10\r\n"
            f"Access-Control-Allow-Origin: *\r\n\r\n"
            f"{master_body}"
        )
        steps.append(ProtocolStep(
            step_id=step_counter,
            protocol="HTTP",
            title="HLS Master Manifest Delivered: 200 OK",
            direction="server_to_client",
            sender=f"CDN Edge ({cdn_ip}:443)",
            receiver=f"Client ({client_ip})",
            time_offset_ms=elapsed,
            summary="Server returns adaptive bitrate manifest listing 1080p, 720p, 480p, and 360p streams.",
            raw_wire=resp_master,
            key_fields={
                "Status": "200 OK",
                "Available Streams": "1080p, 720p, 480p, 360p",
                "Format": "HLS M3U8 Master Index"
            },
            category="media"
        ))
        step_counter += 1
        elapsed += 25

        # 5. HTTP GET Media Playlist
        variant_url = f"/live/hls/{quality}/index.m3u8"
        req_variant = (
            f"GET {variant_url} HTTP/1.1\r\n"
            f"Host: {cdn_host}\r\n"
            f"Connection: keep-alive\r\n\r\n"
        )
        steps.append(ProtocolStep(
            step_id=step_counter,
            protocol="HTTP",
            title=f"HLS Fetch: GET Variant Playlist ({quality})",
            direction="client_to_server",
            sender=f"Client ({client_ip})",
            receiver=f"CDN Edge ({cdn_ip}:443)",
            time_offset_ms=elapsed,
            summary=f"Player selects {quality} ({info['res']} @ {info['bandwidth']//1000}kbps) and requests chunk playlist.",
            raw_wire=req_variant,
            key_fields={
                "Selected Variant": quality,
                "Target Bitrate": f"{info['bandwidth'] // 1000} kbps",
                "Resolution": info["res"]
            },
            category="media"
        ))
        step_counter += 1
        elapsed += 30

        # 6. HTTP 200 Response Media Playlist
        segment_files = [f"segment_{i:03d}.ts" for i in range(1, segment_count + 1)]
        variant_lines = [
            "#EXTM3U",
            "#EXT-X-VERSION:3",
            "#EXT-X-TARGETDURATION:4",
            "#EXT-X-MEDIA-SEQUENCE:104"
        ]
        for seg in segment_files:
            variant_lines.append("#EXTINF:4.000000,")
            variant_lines.append(seg)
        variant_body = "\n".join(variant_lines) + "\n"

        resp_variant = (
            f"HTTP/1.1 200 OK\r\n"
            f"Content-Type: application/vnd.apple.mpegurl\r\n"
            f"Content-Length: {len(variant_body.encode())}\r\n"
            f"Cache-Control: max-age=4\r\n\r\n"
            f"{variant_body}"
        )
        steps.append(ProtocolStep(
            step_id=step_counter,
            protocol="HTTP",
            title=f"HLS Media Playlist ({quality}): 200 OK",
            direction="server_to_client",
            sender=f"CDN Edge ({cdn_ip}:443)",
            receiver=f"Client ({client_ip})",
            time_offset_ms=elapsed,
            summary=f"Received active segment playlist containing {segment_count} media chunks (4.0s each).",
            raw_wire=resp_variant,
            key_fields={
                "Target Duration": "4.0s per chunk",
                "Sequence Start": "104",
                "Segments Available": ", ".join(segment_files)
            },
            category="media"
        ))
        step_counter += 1
        elapsed += 20

        # 7..N Sequential Segment Requests
        for idx, seg in enumerate(segment_files, start=1):
            seg_url = f"/live/hls/{quality}/{seg}"
            req_seg = (
                f"GET {seg_url} HTTP/1.1\r\n"
                f"Host: {cdn_host}\r\n"
                f"Range: bytes=0-\r\n"
                f"Connection: keep-alive\r\n\r\n"
            )
            steps.append(ProtocolStep(
                step_id=step_counter,
                protocol="HTTP",
                title=f"HLS Chunk Request #{idx}: GET {seg}",
                direction="client_to_server",
                sender=f"Client ({client_ip})",
                receiver=f"CDN Edge ({cdn_ip}:443)",
                time_offset_ms=elapsed,
                summary=f"Download video transport stream chunk #{idx} ({quality}).",
                raw_wire=req_seg,
                key_fields={
                    "Chunk Index": f"#{idx}",
                    "Segment URI": seg_url,
                    "Range Support": "bytes=0-"
                },
                category="media"
            ))
            step_counter += 1
            elapsed += 35

            chunk_size = info["chunk_kb"] * 1024
            resp_seg = (
                f"HTTP/1.1 206 Partial Content\r\n"
                f"Content-Type: video/MP2T\r\n"
                f"Content-Range: bytes 0-{chunk_size-1}/{chunk_size}\r\n"
                f"Content-Length: {chunk_size}\r\n"
                f"Connection: keep-alive\r\n"
                f"Accept-Ranges: bytes\r\n"
                f"X-Cache: HIT from edge-cdn\r\n\r\n"
                f"[Binary MPEG-2 Transport Stream: AVC/H.264 Video + AAC Audio (~{info['chunk_kb']} KB)]"
            )
            steps.append(ProtocolStep(
                step_id=step_counter,
                protocol="HTTP",
                title=f"HLS Chunk Delivered #{idx}: 206 Partial Content ({info['chunk_kb']} KB)",
                direction="server_to_client",
                sender=f"CDN Edge ({cdn_ip}:443)",
                receiver=f"Client ({client_ip})",
                time_offset_ms=elapsed,
                summary=f"Loaded segment #{idx} ({info['chunk_kb']} KB). Buffer increased by +4.0s.",
                raw_wire=resp_seg,
                key_fields={
                    "Status": "206 Partial Content",
                    "Content-Type": "video/MP2T",
                    "Payload Size": f"{info['chunk_kb']} KB",
                    "Duration Added": "+4.0 seconds",
                    "Buffer Health": f"{(idx * 4.0):.1f}s buffered"
                },
                category="media"
            ))
            step_counter += 1
            elapsed += 45

        return {
            "activity": "streaming",
            "quality": quality,
            "resolution": info["res"],
            "bitrate_kbps": info["bandwidth"] // 1000,
            "total_segments": segment_count,
            "total_buffered_sec": segment_count * 4.0,
            "total_time_ms": elapsed,
            "steps": [s.to_dict() for s in steps]
        }
