import asyncio
import os
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
def run(file_path: str = typer.Option("events.log", help="Le chemin du fichier log à traiter")):
    """Lancer le traitement asynchrone avec file pipeline"""
    if not os.path.exists(file_path):
        print(f"\033[35m[-] Le fichier spécifié '{file_path}' est introuvable.\033[35m")
        return  # Empêcher la sortie du programme avec SystemExit(2)

    try:
        async def pipeline():
            queue = asyncio.Queue()
            analyzer = EventAnalyzer()
            producer = asyncio.create_task(read_lines(file_path, queue))
            consumer = asyncio.create_task(process_lines(queue, analyzer))
            await producer
            await queue.join()
            consumer.cancel()

        asyncio.run(pipeline())
    except Exception as e:
        print(f"\033[31m[-] Une erreur s'est produite : {e}\033[0m")

@app.command()
def show_alerts():
    """Afficher les alertes sauvegardées"""
    try:
        alerts = load_alerts(config.get("alert_storage.alerts_file_path"))
        if not alerts:
            print("\033[33m[-] Aucune alerte trouvée.\033[0m")
        for a in alerts:
            print(f"\033[32m\n[-->] Alerte à {a.triggered_at}\033[0m")
            for e in a.events:
                print(f"\033[32m[*]   {e.timestamp} | {e.level} | {e.message}\033[0m")
    except Exception as e:
        print(f"\033[31m[-] Une erreur s'est produite : {e}\033[0m")


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
        print("\033[35m[-] Aucun dossier 'reports' trouvé.\033[35m")
        return

    count = 0
    for file in reports_dir.iterdir():
        if file.suffix in {".html", ".pdf", ".png"}:
            file.unlink()
            count += 1
    if count > 0:
        print(f"\033[32m[+] {count} fichier(s) supprimé(s) dans 'reports/'\033[0m")
    else:
        print("\033[35m[-] Aucun fichier de rapport à supprimer.\033[35m")

if __name__ == "__main__":
    app()
