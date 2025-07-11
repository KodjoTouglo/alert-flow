from datetime import datetime

class Event:
    """
        Classe représentant un événement.

        Un événement est une donnée ayant une date et une heure (`timestamp`), un niveau (`level`), et un message (`message`).
        L'événement est créé à partir de données brutes sous forme de dictionnaire.

        Attributs :
        - raw : dict - Dictionnaire contenant les données brutes de l'événement.
        - timestamp : datetime - Le moment où l'événement s'est produit.
        - level : str - Le niveau de l'événement (par exemple, "INFO", "ERROR", "CRITICAL").
        - message : str - Le message associé à l'événement.
    """
    def __init__(self, raw: dict, timestamp_key="timestamp", level_key="level", message_key="message"):
        """
            Initialise un événement à partir des données brutes.

            Cette méthode récupère les valeurs du `timestamp`, `level` et `message` dans le dictionnaire `raw` et les
            convertit selon leur format.

            :param raw: dict - Le dictionnaire contenant les données brutes de l'événement.
            :param timestamp_key: str - La clé du dictionnaire qui contient l'horodatage de l'événement (par défaut "timestamp").
            :param level_key: str - La clé du dictionnaire qui contient le niveau de l'événement (par défaut "level").
            :param message_key: str - La clé du dictionnaire qui contient le message de l'événement (par défaut "message").
        """
        self.raw = raw
        self.timestamp = datetime.fromisoformat(raw[timestamp_key].replace("Z", "+00:00"))
        self.level = raw.get(level_key, "").upper()
        self.message = raw.get(message_key, "")

    def __repr__(self):
        """
            Retourne une représentation sous forme de chaîne de l'événement.

            Cette méthode définit la façon dont l'objet `Event` est représenté sous forme de chaîne lorsque l'on tente
            d'afficher ou de convertir l'objet en une chaîne.

            :return: str - Représentation sous forme de chaîne de l'événement.
        """
        return f"[{self.timestamp}] {self.level} - {self.message}"
