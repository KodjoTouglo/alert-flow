class Config:
    """
        Initialise la configuration avec des valeurs par défaut.

        Lors de l'initialisation de l'objet `Config`, une configuration par défaut est définie avec les
        sections suivantes :
        - event_analyzer : Paramètres liés à l'analyse des événements (fenêtre de temps, niveaux critiques).
        - alert_storage : Paramètres liés au stockage des alertes (chemin du fichier des alertes).
        - reports : Paramètres liés à la génération des rapports (répertoire de sortie, fichiers de rapports PDF et HTML).
    """
    def __init__(self):
        """
            Initialise la configuration avec des valeurs par défaut.

            Lors de l'initialisation de l'objet `Config`, une configuration par défaut est définie avec les
            sections suivantes :
            - event_analyzer : Paramètres liés à l'analyse des événements (fenêtre de temps, niveaux critiques).
            - alert_storage : Paramètres liés au stockage des alertes (chemin du fichier des alertes).
            - reports : Paramètres liés à la génération des rapports (répertoire de sortie, fichiers de rapports PDF et HTML).
        """

        # Définition des valeurs par défaut
        self.config = {
            "event_analyzer": {
                "window_seconds": 30,
                "critical_levels": ["CRITICAL"]
            },
            "alert_storage": {
                "alerts_file_path": "alerts.json"
            },
            "reports": {
                "output_directory": "reports",
                "pdf_report_file": "report.pdf",
                "html_report_file": "report.html"
            }
        }

    def get(self, key: str, default=None):
        """
            Accède à une valeur dans la configuration en utilisant une clé.

            Cette méthode permet d'accéder à une valeur de configuration en utilisant une clé sous forme de chaîne.
            La clé peut contenir des sous-clés séparées par des points (par exemple "event_analyzer.window_seconds").

            :param key: Clé de la configuration (peut être une chaîne avec des sous-clés séparées par des points).
            :param default: Valeur par défaut à retourner si la clé n'est pas trouvée.
            :return: La valeur de la configuration associée à la clé, ou la valeur par défaut si la clé est introuvable.
        """
        keys = key.split(".")
        config_value = self.config
        for key in keys:
            config_value = config_value.get(key, default)
        return config_value

    def __repr__(self):
        """
            Représentation textuelle de l'objet `Config`.

            Cette méthode définit la façon dont l'objet `Config` est représenté sous forme de chaîne.
            Elle renvoie une chaîne qui affiche la structure complète de la configuration.

            :return: Chaîne représentant la configuration.
        """
        return f"<Config {self.config}>"
