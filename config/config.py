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

    @property
    def mock_server_host(self):
        return self.data["mock_server"]["host"]


    @property
    def mock_server_port(self):
        return self.data["mock_server"]["port"]


    @property
    def mock_server_health_endpoint(self):
        return self.data["mock_server"]["health_endpoint"]

    @property
    def rate_limit(self):
        return self.data.get("rate_limit", {})

    # ====================================================
    # Rate Limit Helper Methods
    # ====================================================

    def get_rate_limit(self, endpoint: str) -> dict:
        """
        Returns complete rate limit configuration for an endpoint.
        Falls back to default configuration if endpoint is not configured.
        """

        endpoints = self.rate_limit.get("endpoints", {})
        default = self.rate_limit.get("default", {})

        return endpoints.get(endpoint, default)

    def get_max_requests(self, endpoint: str) -> int:
        """
        Returns max allowed requests for an endpoint.
        """

        return self.get_rate_limit(endpoint)["max_requests"]

    def get_window_seconds(self, endpoint: str) -> int:
        """
        Returns rate limit window (seconds) for an endpoint.
        """

        return self.get_rate_limit(endpoint)["window_seconds"]
    
    def is_rate_limit_enabled(self) -> bool:
        """
        Returns whether rate limiting is enabled.
        """

        return self.rate_limit.get("enabled", False)