from app.models.alerts_model import Alert
from app.providers.alerts_provider import load_alerts

def handle_alert(alert: Alert):
    load_alerts(alert)
