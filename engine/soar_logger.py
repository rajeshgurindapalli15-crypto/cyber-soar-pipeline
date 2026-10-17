import os
import sqlite3
import requests
from datetime import datetime, timezone
from pymongo import MongoClient
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))
dotenv_path = os.path.join(ROOT_DIR, ".env")

load_dotenv(dotenv_path=dotenv_path)

SQLITE_DB = os.path.join(ROOT_DIR, "storage", "threat_intel.db")

MONGO_URI = os.getenv("MONGO_URI")
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

print(f"DEBUG: Root Dir -> {ROOT_DIR}")
print(f"DEBUG: MONGO_URI loaded -> {bool(MONGO_URI)}")

def init_sqlite():
    conn = sqlite3.connect(SQLITE_DB)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS audit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            event_type TEXT,
            source_ip TEXT,
            severity TEXT,
            action_taken TEXT
        )
    ''')
    conn.commit()
    conn.close()
tls_insecure = os.getenv("MONGO_TLS_INSECURE", "false").lower() == "true"

if tls_insecure:
    mongo_client = MongoClient(MONGO_URI, tlsAllowInvalidCertificates=True)
else:
    mongo_client = MongoClient(MONGO_URI)

db = mongo_client["cyber_soar_db"]
alerts_collection = db["security_alerts"]

def send_discord_alert(event_type, source_ip, severity, action_taken, timestamp):
    if not DISCORD_WEBHOOK_URL:
        print("⚠️ [Discord] Webhook URL not found in environment variables. Skipping alert.")
        return

    payload = {
        "embeds": [{
            "title": "🚨 SOAR Security Incident Alert",
            "color": 15158332, 
            "fields": [
                {"name": "Event Type", "value": event_type, "inline": True},
                {"name": "Severity", "value": severity, "inline": True},
                {"name": "Source IP", "value": f"`{source_ip}`", "inline": False},
                {"name": "Action Taken", "value": action_taken, "inline": False},
                {"name": "Timestamp (UTC)", "value": timestamp, "inline": False}
            ],
            "footer": {"text": "Cyber-SOAR Automated Pipeline"}
        }]
    }

    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
        if response.status_code == 204:
            print("💬 [Discord] Real-time alert dispatched successfully.")
        else:
            print(f"❌ [Discord] Failed to send alert: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ [Discord] Error: {e}")

def log_security_event(event_type, source_ip, severity, action_taken):
    timestamp = datetime.now(timezone.utc).isoformat()
    
    event_data = {
        "timestamp": timestamp,
        "event_type": event_type,
        "source_ip": source_ip,
        "severity": severity,
        "action_taken": action_taken
    }

    try:
        conn = sqlite3.connect(SQLITE_DB)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO audit_logs (timestamp, event_type, source_ip, severity, action_taken)
            VALUES (?, ?, ?, ?, ?)
        ''', (timestamp, event_type, source_ip, severity, action_taken))
        conn.commit()
        conn.close()
        print("📁 [SQLite] Local audit log saved successfully.")
    except Exception as e:
        print(f"❌ [SQLite] Error: {e}")

    try:
        alerts_collection.insert_one(event_data)
        print("☁️ [MongoDB Atlas] Cloud security alert published successfully.")
    except Exception as e:
        print(f"❌ [MongoDB Atlas] Error: {e}")

    send_discord_alert(event_type, source_ip, severity, action_taken, timestamp)

if __name__ == "__main__":
    init_sqlite()
    print("🚀 Simulating Full-Spectrum Security Incident Response Event...")
    
    log_security_event(
        event_type="Brute-Force SSH Attack",
        source_ip="192.168.1.105",
        severity="High",
        action_taken="Blocked via Firewall & Notified via Discord"
    )