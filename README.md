# Alert Flow

**Alert Flow** est un outil de traitement asynchrone des événements et de gestion des alertes. Il permet de lire des fichiers log, d'analyser les événements, de détecter des alertes et de générer des rapports en format HTML ou PDF. Il utilise un système de pipeline pour traiter les événements en temps réel.

## Structure du Projet
```
alert-flow/
├── reports/        # contient le document pdf, html, les graphiques, ...
│
├── src/
│ └── app/
│ ├── configs/      # Configuration de l'application
│ ├── models/       # Modèles de données (par exemple, Event, Alert)
│ ├── providers/    # Fournisseurs de données (chargement des logs, alertes, etc.)
│ ├── services/     # Logique métier pour l'analyse des événements, la détection des alertes, etc.
│
├── alerts.json     # le fichier log contenant les alertes
├── setup.py        # Script d'installation du package
├── main.py         # Point d'entrée de l'application
└── README.md       # Ce fichier README
```


## Prérequis

Le projet nécessite **Python 3.10 ou supérieur** pour fonctionner.

### Dépendances

- **Typer** : Pour créer l'interface en ligne de commande (CLI).
- **Asyncio** : Pour le traitement asynchrone des événements.
- **Matplotlib** : Pour la génération de graphiques dans les rapports.
- **Pandas** : Pour la manipulation et l'analyse des événements.
- **Fpdf** : Pour la génération de rapports PDF.
- **Aiofiles** : Pour lire les fichiers log de manière asynchrone.

### Installation

1. **Clonez le projet** dans votre répertoire local :

   ```bash
   git clone https://github.com/KodjoTouglo/alert-flow.git
   cd alert-flow
   ```

2. **Créer un environnement virtuel (optionnel mais recommandé)**
   ```bash
   python3.10 -m venv alert-flow
   source alert-flow/bin/activate   # sur Windows : alert-flow\Scripts\activate
   ```
3. **Installez les dépendances de développement** :

   ```bash
   pip install -r requirements.txt
   ```

4. **Installez le package avec `setup.py`** :

   Assurez-vous d'avoir **Python 3.10** ou une version plus récente installée. Ensuite, installez le projet via `setup.py` :

   ```bash
   python setup.py install
   ```

5. **Vérifiez l'installation** :

   Une fois l'installation terminée, vous pouvez vérifier que le package a bien été installé et que l'application fonctionne en exécutant :

   ```bash
   python main.py --help
   ```

   Cela vous donnera un aperçu des commandes disponibles dans l'application.

---

## Commandes Disponibles

L'application utilise **Typer** pour gérer les commandes en ligne de commande. Voici les principales commandes disponibles :

### 1. `run` - Lancer le traitement asynchrone des événements

```bash
python main.py run --file-path <fichier_log>
```

Cette commande lance un pipeline asynchrone pour analyser le fichier log spécifié. Par défaut, si aucun fichier n'est spécifié, le fichier `events.log` est utilisé.

**Arguments** :

- `fichier_log` (facultatif) : Le chemin du fichier log à traiter. Par défaut, `events.log` est utilisé.

### 2. `show-alerts` - Afficher les alertes sauvegardées

```bash
python main.py show-alerts
```

Cette commande affiche toutes les alertes sauvegardées dans le fichier `alerts.json`.

### 3. `report` - Générer un rapport PDF avec un graphique

```bash
python main.py report
```

Cette commande génère un rapport au format PDF avec un graphique représentant la distribution des événements.

### 4. `html` - Générer un rapport HTML interactif

```bash
python main.py html
```

Cette commande génère un rapport au format HTML interactif, avec un graphique et la possibilité de filtrer les événements par niveau (INFO, ERROR, CRITICAL, etc.).

### 5. `clean-reports` - Nettoyer les rapports (HTML, PDF, PNG)

```bash
python main.py clean-reports
```

Cette commande supprime tous les fichiers de rapport (HTML, PDF et PNG) générés dans le répertoire de rapports.

---

## Structure du Code

Le code est organisé comme suit :

- **`configs/`** : Contient les fichiers de configuration pour l'application.
- **`models/`** : Contient les modèles de données (par exemple, `Event`, `Alert`).
- **`providers/`** : Contient les fournisseurs de données (chargement des événements depuis les fichiers log, récupération des alertes).
- **`services/`** : Contient la logique métier pour l'analyse des événements, la détection des alertes et la génération des rapports.
- **`main.py`** : Point d'entrée de l'application qui utilise **Typer** pour gérer les commandes en ligne de commande.

---

## Notes Supplémentaires :

- **Exécution** : Assurez-vous que tous les prérequis sont bien installés et que Python 3.10 ou plus récent est utilisé.
- **Logs** : Le fichier log par défaut est `events.log`. Vous pouvez spécifier un autre fichier en utilisant la commande `run --file-path <fichier_log>`.
- **Rapports** : Les rapports PDF et HTML sont générés dans le répertoire `reports/` et peuvent être nettoyés avec la commande `clean-reports`.