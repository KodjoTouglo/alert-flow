import asyncio
from datetime import datetime
from pathlib import Path

import typer

from app.configs.config import Config
from app.providers.alerts_provider import load_alerts
from app.providers.events_provider import load_events
from app.services.events_analyzer import EventAnalyzer
from app.services.process.process_lines import process_lines
from app.services.process.read import read_lines
from app.services.process.report_generator import generate_pdf, generate_html

app = typer.Typer()

# Charger la configuration
config = Config()

@app.command()
def run(file_path: str = "events.log"):
    """Lancer le traitement asynchrone avec file pipeline"""
    async def pipeline():
        queue = asyncio.Queue()
        analyzer = EventAnalyzer()
        producer = asyncio.create_task(read_lines(file_path, queue))
        consumer = asyncio.create_task(process_lines(queue, analyzer))
        await producer
        await queue.join()
        consumer.cancel()

    asyncio.run(pipeline())

@app.command()
def show_alerts():
    """Afficher les alertes sauvegardées"""
    alerts = load_alerts(config.get("alert_storage.alerts_file_path"))
    for a in alerts:
        print(f"\n[-->] Alerte à {a.triggered_at}")
        for e in a.events:
            print(f"[*]   {e.timestamp} | {e.level} | {e.message}")

@app.command()
def report():
    """Générer un rapport PDF avec graphique"""
    events = load_events()
    alerts = load_alerts(config.get("alert_storage.alerts_file_path"))
    generate_pdf(events, alerts)

@app.command()
def html():
    """Générer un rapport HTML interactif horodaté"""
    events = load_events()
    alerts = load_alerts(config.get("alert_storage.alerts_file_path"))
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    graph_path = f"{config.get('reports.output_directory')}/event_distribution_{timestamp}.png"
    html_path = f"{config.get('reports.output_directory')}/report_{timestamp}.html"
    generate_html(events, alerts, graph_path, html_path)

@app.command()
def clean_reports():
    """Nettoyer les fichiers de rapport HTML/PDF/graphique"""
    reports_dir = Path(config.get("reports.output_directory"))
    if not reports_dir.exists():
        print("[-] Aucun dossier 'reports' trouvé.")
        return

    count = 0
    for file in reports_dir.iterdir():
        if file.suffix in {".html", ".pdf", ".png"}:
            file.unlink()
            count += 1
    print(f"[+] {count} fichier(s) supprimé(s) dans 'reports/'")

if __name__ == "__main__":
    app()
