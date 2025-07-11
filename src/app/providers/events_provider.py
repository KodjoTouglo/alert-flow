import json

from app.models.event_model import Event


def load_events(file_path="events.log") -> list[Event]:
    """
        Charge les événements depuis un fichier log.

        Cette fonction lit un fichier log ligne par ligne et tente de décoder chaque ligne
        en format JSON. Chaque ligne qui est correctement décodée est ensuite utilisée pour
        créer un objet `Event`, qui est ajouté à une liste d'événements.

        :param file_path: str - Le chemin du fichier log à lire (par défaut "events.log").
        :return: List[Event] - Liste des objets `Event` créés à partir des données du fichier log.
    """
    events = []
    with open(file_path, "r") as f:
        for line in f:
            try:
                data = json.loads(line)
                events.append(Event(data))
            except:
                continue
    return events
