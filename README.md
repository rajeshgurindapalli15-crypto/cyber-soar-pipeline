# 🛡️ Cloud-Native SOAR: Automated Threat Detection & Incident Response Pipeline

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Database](https://img.shields.io/badge/Storage-SQLite3%20%7C%20MongoDB%20Atlas-green.svg?style=for-the-badge&logo=mongodb&logoColor=white)](https://www.mongodb.com/)
[![Alerting](https://img.shields.io/badge/Alerts-Discord%20Webhooks-5865F2.svg?style=for-the-badge&logo=discord&logoColor=white)](https://discord.com/)
[![License](https://img.shields.io/badge/License-MIT-brightgreen.svg?style=for-the-badge)](LICENSE)
[![DevSecOps Compliance](https://img.shields.io/badge/Compliance-ISO%208601%20UTC-orange.svg?style=for-the-badge)](#)

A production-grade **Security Orchestration, Automation, and Response (SOAR)** framework designed to ingest threat telemetry, execute automated mitigation playbooks, maintain hybrid audit logging (edge and cloud), and dispatch real-time incident notifications to Security Operations Center (SOC) teams.


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
## 🚀 Live Operational Execution & Verification

Below is the sequential end-to-end operational proof demonstrating the `cyber-soar-pipeline` intercepting security threats, executing automated playbooks, persisting audit trails locally, and synchronizing data to the cloud in real-time.

## Step 1: Automated SOAR Playbook Execution
When a security incident is triggered from the CLI, the pipeline initializes, logs locally to SQLite, publishes threat intelligence to MongoDB Atlas, and dispatches an instant webhook alert[cite: 7, 10].

![SOAR Playbook Execution](assets/soar_execution_output.png)


## Step 2: Automated Unit Testing
The system validates component resilience and data structures via automated `pytest` execution.

![Pytest Suite Passed](assets/soar_pytest_output.png)


## Step 3: Local Edge Audit Log Persistence (SQLite)
Edge auditing records individual and multi-vector security events locally for immediate forensic inspection.

![SQLite Edge Audit Table](assets/soar_sqlite_output.png)


## Step 4: Local Edge Persistence (SQLite)
Below is the tabular inspection of local audit logs using **DB Browser for SQLite**:

![SQLite DB Browser View](assets/soar_sqlite_gui_output.png)


## Step 5: Centralized Cloud Threat Intelligence (MongoDB Atlas CLI View)
The CLI queries the cloud cluster to render a consolidated view of global threat intelligence via Rich tables.

![MongoDB CLI Threat View](assets/soar_mongo_cli_output.png)


## Step 6: Cloud Dashboard Persistence (MongoDB Atlas Cloud UI)
Live document storage verified directly within the MongoDB Atlas cloud cluster dashboard, displaying structured JSON audit documents.

![MongoDB Atlas Dashboard UI](assets/soar_mongodb_atlas_ui.png)


## Step 7. Automated Real-Time Alerting (Discord Webhook)
Demonstrates automated, real-time incident dispatches triggered via Discord webhooks upon threat detection. The pipeline formats dynamic JSON payloads with rich contextual telemetry—including attacker IP, geographical origin, ISP details, and automated firewall mitigation strategies—enabling immediate visibility for SOC analysts.

![Discord Real-Time Alert Output](assets/soar_discord_alert_output.png)






