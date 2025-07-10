from typing import List
from app.models.alerts_model import Alert
import json
from datetime import datetime
from .events_provider import Event

def load_alerts(path="alerts.json") -> List[Alert]:
    try:
        with open(path, "r") as f:
            data = f.read().strip()  # Lire et retirer les espaces blancs
            if not data:  # Vérifie si le fichier est vide
                print(f"[-] Le fichier {path} est vide.")
                return []  # Retourner une liste vide si le fichier est vide

            alerts_data = json.loads(data)
            return [Alert(triggered_at=datetime.fromisoformat(d["triggered_at"]),
                          events=[Event(e) for e in d["events"]]) for d in alerts_data]
    except FileNotFoundError:
        print(f"[-] Le fichier {path} est introuvable.")
        return []  # Retourner une liste vide si le fichier n'existe pas
    except json.JSONDecodeError as e:
        print(f"[-] Erreur de décodage JSON dans {path}: {e}")
        return []  # Retourner une liste vide en cas d'erreur de parsing

def save_alert(alert: Alert, path="alerts.json"):
    """Sauvegarde une alerte dans le fichier alerts.json."""
    try:
        with open(path, "r") as f:
            alerts = json.load(f)
    except FileNotFoundError:
        alerts = []

    alerts.append(alert.to_dict())

    with open(path, "w") as f:
        json.dump(alerts, f, indent=2)
