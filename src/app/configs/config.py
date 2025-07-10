import json
from pathlib import Path


class Config:
    def __init__(self, config_path="configs/default_config.json"):
        self.config_path = Path(config_path)
        self.config = self.load_config()

    def load_config(self):
        """Charge la configuration à partir du fichier JSON."""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Le fichier de configuration '{self.config_path}' est introuvable.")

        with open(self.config_path, "r") as f:
            return json.load(f)

    def get(self, key: str, default=None):
        """Permet d'accéder à une valeur dans la configuration."""
        keys = key.split(".")
        config_value = self.config
        for key in keys:
            config_value = config_value.get(key, default)
        return config_value

    def __repr__(self):
        return f"<Config {self.config}>"
