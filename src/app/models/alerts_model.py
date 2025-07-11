from datetime import datetime

from .event_model import Event


class Alert:
    """
        Classe représentant une alerte.

        Une alerte est déclenchée à un moment spécifique (`triggered_at`) et contient une liste d'événements qui
        ont conduit à cette alerte. Chaque événement est représenté par un objet `Event`.

        Attributs :
        - triggered_at : datetime - Le moment où l'alerte a été déclenchée.
        - events : list[Event] - Liste des événements associés à l'alerte.
    """
    def __init__(self, triggered_at: datetime, events: list[Event]):
        """
            Initialise une nouvelle alerte.

            :param triggered_at: datetime - La date et l'heure auxquelles l'alerte a été déclenchée.
            :param events: list[Event] - La liste des événements associés à l'alerte.
        """
        self.triggered_at = triggered_at
        self.events = events

    def to_dict(self):
        """
            Convertit l'alerte en un dictionnaire.

            Cette méthode permet de convertir l'objet `Alert` en un dictionnaire afin de faciliter la sérialisation
            de l'alerte en JSON. Les objets `datetime` sont convertis en chaînes ISO 8601 et les événements sont
            convertis en leurs représentations brutes (raw).

            :return: dict - Représentation de l'alerte sous forme de dictionnaire.
        """
        return {
            "triggered_at": self.triggered_at.isoformat(), # Convertit datetime en chaîne ISO 8601
            "events": [e.raw for e in self.events] # Sérialisation des événements associés
        }
