from pathlib import Path
from importlib.metadata import version, PackageNotFoundError
import platform

from config.version import FRAMEWORK_VERSION


class AllureEnvironment:

    @staticmethod
    def _get_package_version(package_name: str) -> str:
        """
        Returns installed package version.
        Returns 'Unknown' if package is not installed.
        """
        try:
            return version(package_name)

        except PackageNotFoundError:
            return "Unknown"

    @classmethod
    def write(
        cls,
        environment: str,
        base_url: str
    ):

        results_dir = Path("allure-results")
        results_dir.mkdir(exist_ok=True)

        properties = {

            "Environment": environment,

            "Base URL": base_url,

            "Python": platform.python_version(),

            "Operating System":
                f"{platform.system()} {platform.release()}",

            "Pytest":
                cls._get_package_version("pytest"),

            "Playwright":
                cls._get_package_version("playwright"),

            "Pydantic":
                cls._get_package_version("pydantic"),

            "Faker":
                cls._get_package_version("faker"),

            "Framework Version":
                FRAMEWORK_VERSION
        }

        environment_file = results_dir / "environment.properties"

        with open(
            environment_file,
            "w",
            encoding="utf-8"
        ) as file:

            for key, value in properties.items():
                file.write(f"{key}={value}\n")