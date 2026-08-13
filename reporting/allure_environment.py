from pathlib import Path
from importlib.metadata import version, PackageNotFoundError
import platform

from config.framework_info import FrameworkInfo


class AllureEnvironment:

    @staticmethod
    def _get_package_version(package_name: str) -> str:
        """
        Returns the installed package version.
        Returns 'Unknown' if the package is not installed.
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
    ) -> None:

        results_dir = Path("allure-results")
        results_dir.mkdir(parents=True, exist_ok=True)

        # Framework metadata
        framework_name = FrameworkInfo.name()
        framework_version = FrameworkInfo.version()

        # Environment properties
        properties = {

            "Framework": framework_name,

            "Framework Version": framework_version,

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
                cls._get_package_version("faker")
        }

        environment_file = results_dir / "environment.properties"

        content = "\n".join(
            f"{key}={value}"
            for key, value in properties.items()
        )

        environment_file.write_text(
            content,
            encoding="utf-8"
        )