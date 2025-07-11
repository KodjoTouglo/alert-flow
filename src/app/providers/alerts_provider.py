import json
from datetime import datetime
from pathlib import Path
from threading import Lock

from app.models.alerts_model import Alert
from .events_provider import Event

# Création d'un verrou global
lock = Lock()


def load_alerts(path="alerts.json") -> list[Alert]:
    """
        Charge les alertes depuis un fichier JSON.

        Cette fonction lit le fichier spécifié, puis tente de décoder son contenu JSON
        pour créer une liste d'objets `Alert`. Si le fichier est introuvable, vide ou
        contient des erreurs de formatage, une liste vide est renvoyée.

        :param path: str - Le chemin du fichier contenant les alertes (par défaut "alerts.json").
        :return: List[Alert] - Une liste d'objets `Alert` chargés depuis le fichier.
    """
    try:
        with open(path, "r") as f:
            data = f.read().strip()  # Lire et retirer les espaces blancs
            if not data:  # Vérifie si le fichier est vide
                print(f"\033[35m[-] Le fichier {path} est vide.\033[35m")
                return []  # Retourner une liste vide si le fichier est vide

            alerts_data = json.loads(data)
            return [Alert(triggered_at=datetime.fromisoformat(d["triggered_at"]),
                          events=[Event(e) for e in d["events"]]) for d in alerts_data]
    except FileNotFoundError:
        print(f"\033[35m[-] Le fichier {path} est introuvable.\033[35m")
        return []  # Retourner une liste vide si le fichier n'existe pas
    except json.JSONDecodeError as e:
        print(f"\033[35m[-] Erreur de décodage JSON dans {path}: {e}\033[35m")
        return []  # Retourner une liste vide en cas d'erreur de parsing


def save_alerts(alert, path="alerts.json"):
    """
        Sauvegarde une alerte dans un fichier JSON.

        Cette fonction prend une alerte et l'ajoute au fichier spécifié. Si le fichier
        existe déjà, les alertes existantes seront chargées et la nouvelle alerte y sera
        ajoutée. Si le fichier n'existe pas, un nouveau fichier sera créé.

        :param alert: Alert - L'alerte à sauvegarder.
        :param path: str - Le chemin du fichier où les alertes seront sauvegardées (par défaut "alerts.json").
    """
    try:
        # Acquérir le verrou avant de manipuler le fichier
        with lock:
            # Vérifier si le fichier existe déjà
            if Path(path).exists():
                with open(path, "r") as f:
                    alerts = json.load(f)
            else:
                alerts = []

            # Ajouter la nouvelle alerte à la liste
            alerts.append(alert.to_dict())

            # Sauvegarder les alertes dans le fichier
            with open(path, "w") as f:
                json.dump(alerts, f, indent=2)

            print(f"\033[32m[+] Alerte sauvegardée à {path}\033[0m")
    except Exception as e:
        print(f"\033[35mErreur lors de la sauvegarde de l'alerte: {e}\033[35m")
