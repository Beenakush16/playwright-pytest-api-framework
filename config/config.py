from pathlib import Path
import yaml

class Config:
    def __init__(self, env:str):
        self.environment = env
        config_path = Path(__file__).parent / "environments" / f"{env}.yml"

        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file for environment '{env}' not found at {config_path}")

        with open(config_path, 'r') as file:
            self.data = yaml.safe_load(file)

    @property
    def base_url(self):
        return self.data["base_url"]

    @property
    def timeout(self):
        return self.data["timeout"]

    @property
    def headers(self):
        return self.data["headers"]

    @property
    def verify_ssl(self):
        return self.data["verify_ssl"]

    @property
    def retry(self):
        return self.data.get("retry", {})

    