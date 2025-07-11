import datetime
import json
import os

import pytest

from app.models.alerts_model import Alert
from app.models.event_model import Event
from app.providers.alerts_provider import save_alerts


@pytest.fixture
def alert_sample():
    # Création d'une alerte fictive
    event = Event({
        'timestamp': datetime.datetime.utcnow().isoformat(),
        'level': 'CRITICAL',
        'message': 'Test event'
    })
    alert = Alert(triggered_at=datetime.datetime.utcnow(), events=[event])  # Garder un objet datetime ici
    return alert

def test_save_alert(alert_sample):
    alert_path = "test_alerts.json"

    # Nettoyer le fichier d'alertes avant chaque test
    if os.path.exists(alert_path):
        os.remove(alert_path)

    # Sauvegarder l'alerte
    save_alerts(alert_sample, alert_path)

    # Vérifier si l'alerte a été correctement sauvegardée dans le fichier
    with open(alert_path, "r") as f:
        alerts = json.load(f)
        assert len(alerts) == 1  # Vérifier qu'une seule alerte est présente
        # Convertir la chaîne ISO 8601 en datetime avant la comparaison
        saved_triggered_at = datetime.datetime.fromisoformat(alerts[0]["triggered_at"])
        assert saved_triggered_at == alert_sample.triggered_at

    # Nettoyage du fichier après test
    os.remove(alert_path)