class Config:
    def __init__(self):
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
        """Accéder à une valeur dans la configuration."""
        keys = key.split(".")
        config_value = self.config
        for key in keys:
            config_value = config_value.get(key, default)
        return config_value

    def __repr__(self):
        return f"<Config {self.config}>"
