import os
import time
import random
from datetime import datetime, timezone

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE_PATH = os.path.join(BASE_DIR, "../tests/auth.log")

ATTACK_IPS = [
    "46.165.230.5",  
    "18.204.45.12",  
    "185.220.101.5", 
    "91.219.236.4"   
]

def simulate_brute_force(ip):
    print(f"[⚔️] Launching automated Brute-Force Emulation vector from IP: {ip}")
    with open(LOG_FILE_PATH, "a") as file:
        for i in range(3):
            utc_timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
            log_line = f"{utc_timestamp} Failed password for root from {ip} port 49231 ssh2\n"
            file.write(log_line)
            file.flush()
            print(f"    -> Injected authentication failure line {i+1}/3 at {utc_timestamp}")
            time.sleep(1)

def simulate_directory_scan(ip):
    print(f"[⚔️] Launching automated Web Directory Reconnaissance emulation from IP: {ip}")
    paths = ["/admin/config", "/phpmyadmin", "/etc/passwd"]
    with open(LOG_FILE_PATH, "a") as file:
        for path in paths:
            utc_timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
            log_line = f"{utc_timestamp} Directory Scan hit {path} from {ip}\n"
            file.write(log_line)
            file.flush()
            print(f"    -> Injected unauthorized traversal signature for {path} at {utc_timestamp}")
            time.sleep(1)

def run_adversarial_suite():
    print("[*] Adversarial Threat Emulation Framework initialized.")
    print("[*] Target system data stream tied to: " + LOG_FILE_PATH)
    print("--------------------------------------------------")
    
    while True:
        target_ip = random.choice(ATTACK_IPS)
        attack_type = random.choice(["brute", "scan"])
        
        if attack_type == "brute":
            simulate_brute_force(target_ip)
        else:
            simulate_directory_scan(target_ip)
            
        print("[✔] Attack campaign batch committed. Cooling down for next cycle...")
        print("--------------------------------------------------")
        time.sleep(12)

if __name__ == "__main__":
    run_adversarial_suite()