import asyncio
import json


from app.models.event_model import Event
from app.providers.alerts_provider import save_alerts
from app.services.events_analyzer import EventAnalyzer


async def process_lines(queue: asyncio.Queue, analyzer: EventAnalyzer, alert_path: str = "alerts.json"):
    """Consomme les lignes de la queue, analyse les événements et sauvegarde les alertes"""
    while True:
        line = await queue.get()
        try:
            raw = json.loads(line)  # Convertir la ligne en JSON
            event = Event(raw)  # Créer un événement à partir des données
            print(event)  # Afficher l'événement
            alert = analyzer.analyze(event)  # Analyser l'événement pour détecter une alerte
            if alert:
                print(f"\033[32m[*] Alerte : {alert.triggered_at} ({len(alert.events)} événements)\033[0m")
                save_alerts(alert, alert_path)  # Sauvegarder l'alerte
        except Exception as e:
            print(f"\033[35m[-] Erreur : {e}\033[35m")  # Afficher l'erreur en cas d'exception
        finally:
            queue.task_done()  # Marquer la tâche comme terminée
