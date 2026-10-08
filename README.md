# Cloud-Native Automated Threat Detection and Incident Response Pipeline

## Project Overview
An automated Security Orchestration, Automation, and Response (SOAR) pipeline designed to ingest raw system telemetry, detect adversarial signatures, execute immediate firewall edge mitigations, and archive structured logs to a relational database layer.

## Tech Stack and Core Architecture
- **Programming Language:** Python 3.14
- **Database Layer:** SQLite3 Relational Threat Intelligence Repository
- **Security Integration:** Discord Webhook API Architecture
- **Mitigation Protocols:** Automated Firewall Drop Rule Simulation (IP Tables / NACLs)
- **Telemetry Processing:** Real-Time Log File Ingestion Parsing

## Live Production Proof
Below is the live operational verification showing the SOAR pipeline intercepting an active multi-line Brute-Force Authentication Threat and broadcasting high-fidelity data to the target monitoring endpoint:

![Live Discord Security Alert](soar_alert_output.png)
