import click
import sqlite3
import os
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from pymongo import MongoClient
from dotenv import load_dotenv
from soar_logger import log_security_event, init_sqlite, SQLITE_DB

load_dotenv()
console = Console()

@click.group()
def cli():
    """🛡️ Cyber-SOAR Automated Incident Response & Threat Intelligence CLI"""
    pass

@cli.command()
@click.option('--type', default='Brute-Force SSH Attack', help='Type of security event.')
@click.option('--ip', default='192.168.1.105', help='Attacker source IP address.')
@click.option('--severity', default='High', type=click.Choice(['Low', 'Medium', 'High', 'Critical']), help='Incident severity level.')
@click.option('--action', default='Blocked via Firewall & Notified via Discord', help='Action taken.')
def trigger(type, ip, severity, action):
    """Simulate and dispatch a live security alert across the hybrid pipeline."""
    init_sqlite()
    console.print(Panel.fit("🚀 Executing Automated SOAR Playbook...", title="SOAR Engine", border_style="cyan"))
    log_security_event(type, ip, severity, action)
    console.print("[green]✔ Incident successfully processed across SQLite, MongoDB Atlas, and Discord![/green]")

@cli.command()
def view_sqlite():
    """Inspect local edge audit logs stored in SQLite."""
    if not os.path.exists(SQLITE_DB):
        console.print("[red]❌ Local SQLite database not found. Run a trigger command first.[/red]")
        return
    
    conn = sqlite3.connect(SQLITE_DB)
    cursor = conn.cursor()
    cursor.execute("SELECT timestamp, event_type, source_ip, severity, action_taken FROM audit_logs ORDER BY id DESC LIMIT 10")
    rows = cursor.fetchall()
    conn.close()

    table = Table(title="📁 Local SQLite Edge Audit Logs")
    table.add_column("Timestamp (UTC)", style="dim")
    table.add_column("Event Type", style="bold cyan")
    table.add_column("Source IP", style="yellow")
    table.add_column("Severity", style="bold red")
    table.add_column("Action Taken", style="green")

    for row in rows:
        table.add_row(row[0], row[1], row[2], row[3], row[4])
    
    console.print(table)

@cli.command()
def view_mongo():
    """Inspect centralized cloud threat intelligence stored in MongoDB Atlas."""
    mongo_uri = os.getenv("MONGO_URI")
    if not mongo_uri:
        console.print("[red]❌ MONGO_URI missing in environment variables.[/red]")
        return
    
    try:
        client = MongoClient(mongo_uri)
        db = client["cyber_soar_db"]
        alerts = db["security_alerts"].find().sort("_id", -1).limit(10)

        table = Table(title="☁️ MongoDB Atlas Central Threat Intelligence")
        table.add_column("Timestamp (UTC)", style="dim")
        table.add_column("Event Type", style="bold cyan")
        table.add_column("Source IP", style="yellow")
        table.add_column("Severity", style="bold red")
        table.add_column("Action Taken", style="green")

        for alert in alerts:
            table.add_row(
                str(alert.get("timestamp")),
                str(alert.get("event_type")),
                str(alert.get("source_ip")),
                str(alert.get("severity")),
                str(alert.get("action_taken"))
            )
        console.print(table)
    except Exception as e:
        console.print(f"[red]❌ Error connecting to MongoDB Atlas: {e}[/red]")

if __name__ == "__main__":
    cli()