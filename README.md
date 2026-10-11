# 🛡️ Cloud-Native SOAR: Automated Threat Detection & Incident Response Pipeline

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Database](https://img.shields.io/badge/Storage-SQLite%20%7C%20MongoDB%20Atlas-green.svg?style=for-the-badge&logo=mongodb&logoColor=white)](https://www.mongodb.com/)
[![Alerting](https://img.shields.io/badge/Alerts-Discord%20Webhooks-5865F2.svg?style=for-the-badge&logo=discord&logoColor=white)](https://discord.com/)
[![License](https://img.shields.io/badge/License-MIT-brightgreen.svg?style=for-the-badge)](LICENSE)
[![DevSecOps Compliance](https://img.shields.io/badge/Compliance-ISO%208601%20UTC-orange.svg?style=for-the-badge)](#)

A production-grade **Security Orchestration, Automation, and Response (SOAR)** framework designed to ingest threat telemetry, execute automated mitigation playbooks, maintain hybrid audit logging (edge and cloud), and dispatch real-time incident notifications to Security Operations Center (SOC) teams.

---

## 🏗️ Technical Architecture & Workflow

The pipeline utilizes a hybrid storage architecture: local edge logging to **SQLite3** ensures low-latency fault tolerance during network partitioning, while cloud synchronization to **MongoDB Atlas** maintains a centralized threat intelligence database.

```mermaid
flowchart TD
    A[Telemetry / Attack Event] -->|Inbound IP & Vector| B[CLI / Engine Ingestion]
    B --> C{SOAR Orchestration Engine}
    
    C -->|Local Edge Logging| D[(SQLite Audit Log)]
    C -->|Cloud Threat Sync| E[(MongoDB Atlas Cluster)]
    C -->|Webhook Alerting| F[Discord SOC Notification]
    C -->|Mitigation Engine| G[Firewall / NACL Rule Block]
```
## Live Production Proof
Below is the live operational verification showing the SOAR pipeline intercepting an active multi-line Brute-Force Authentication Threat and broadcasting high-fidelity data to the target monitoring endpoint:

![Live Discord Security Alert](soar_alert_output.png)
