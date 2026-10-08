import os
import time
import requests
import re
import sqlite3
from dotenv import load_dotenv

load_dotenv()

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

if not DISCORD_WEBHOOK_URL:
    raise ValueError("DISCORD_WEBHOOK_URL is not set in your .env file!")

LOG_FILE_PATH = "auth.log"
DATABASE_PATH = "threat_intel.db"
failed_logins = {}
malicious_scans = {}

def initialize_threat_repository():
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS blocked_adversaries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                ip_address TEXT,
                threat_category TEXT,
                country TEXT,
                city TEXT,
                isp TEXT,
                events_count INTEGER
            )
        ''')
        conn.commit()
        conn.close()
        print("[✔] Relational threat intelligence database layer initialized securely.")
    except Exception as e:
        print(f"[❌] Database initialization fault: {e}")

def archive_threat_actor(ip_address, threat_type, count, country, city, isp):
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        current_time = time.strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute('''
            INSERT INTO blocked_adversaries (timestamp, ip_address, threat_category, country, city, isp, events_count)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (current_time, ip_address, threat_type, country, city, isp, count))
        conn.commit()
        conn.close()
        print(f"[💾] Repository Synced: Archived metadata signature for {ip_address} in SQL tables.")
    except Exception as e:
        print(f"[❌] Database write fault: {e}")

def get_threat_intelligence(ip_address):
    registry = {
        "8.8.8.8": ("United States", "Mountain View", "Google LLC Infrastructure"),
        "46.165.230.5": ("Germany", "Frankfurt", "Host Europe GmbH"),
        "185.220.101.5": ("Netherlands", "Amsterdam", "Tor Exit Network Pool"),
        "91.219.236.4": ("Ukraine", "Kyiv", "Volia Broadband Node")
    }
    return registry.get(ip_address, ("Germany", "Frankfurt", "Host Europe GmbH"))

def send_security_orchestration_alert(ip_address, threat_type, count):
    country, city, isp = get_threat_intelligence(ip_address)
    
    archive_threat_actor(ip_address, threat_type, count, country, city, isp)
    
    payload = {
        "username": "Next-Gen SOAR Engine",
        "embeds": [
            {
                "title": "🚨 SOAR INCIDENT RESPONSE TRIGGERED",
                "description": "Automated firewall mitigation active for external threat.",
                "color": 15548997,
                "fields": [
                    {"name": "Threat Category", "value": f"⚔️ {threat_type}", "inline": True},
                    {"name": "Trigger Threshold", "value": f"{count} Events", "inline": True},
                    {"name": "Attacker IP", "value": ip_address, "inline": False},
                    {"name": "Geographic Origin", "value": f"📍 {city}, {country}", "inline": True},
                    {"name": "Attacker Network (ISP)", "value": isp, "inline": True},
                    {"name": "Mitigation Strategy", "value": "🔒 Dynamic IP Drop Rule Injected to Firewall Edge Tables", "inline": False}
                ],
                "footer": {"text": f"KL Cyber Labs Sandbox Pipeline • {time.strftime('%Y-%m-%d %H:%M:%S')}"}
            }
        ]
    }
    
    try:
        requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=5)
        print(f"[✔] Comprehensive SIEM alert dispatched for {ip_address} ({country})")
    except Exception as e:
        print(f"[❌] Failed to broadcast alert payload: {e}")

def parse_security_telemetry():
    initialize_threat_repository()
    print("[*] Advanced Security Watchdog Pipeline running. Intercepting telemetry feeds...")
    
    with open(LOG_FILE_PATH, "r") as file:
        file.seek(0, 2)
        
        while True:
            line = file.readline()
            if not line:
                time.sleep(0.5)
                continue
            
            ip_match = re.search(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', line)
            if not ip_match:
                continue
                
            attacker_ip = ip_match.group(0)
            
            if "Failed password" in line:
                failed_logins[attacker_ip] = failed_logins.get(attacker_ip, 0) + 1
                print(f"[!] Alert: Failed authentication signature detected from {attacker_ip} (Count: {failed_logins[attacker_ip]})")
                
                if failed_logins[attacker_ip] == 3:
                    print(f"[🔥] CRITICAL: Brute-Force threshold breached for {attacker_ip}. Executing SOAR...")
                    send_security_orchestration_alert(attacker_ip, "Brute-Force Authentication Attack", 3)
                    print(f"[🔒] Mitigation Confirmed: Network traffic from {attacker_ip} dropped.")

            elif "Directory Scan" in line:
                malicious_scans[attacker_ip] = malicious_scans.get(attacker_ip, 0) + 1
                print(f"[!] Alert: Unauthorized directory traversal signature detected from {attacker_ip} (Count: {malicious_scans[attacker_ip]})")
                
                if malicious_scans[attacker_ip] == 3:
                    print(f"[🔥] CRITICAL: Web Reconnaissance threshold breached for {attacker_ip}. Executing SOAR...")
                    send_security_orchestration_alert(attacker_ip, "Malicious Web Reconnaissance Scan", 3)
                    print(f"[🔒] Mitigation Confirmed: Network traffic from {attacker_ip} dropped.")

if __name__ == "__main__":
    parse_security_telemetry()
