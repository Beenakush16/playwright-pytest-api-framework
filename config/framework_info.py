from importlib.metadata import PackageNotFoundError
from importlib.metadata import version

from pathlib import Path
import tomllib


class FrameworkInfo:

    @staticmethod
    def version():

        # When installed as a package
        try:
            return version("playwright-pytest-api-framework")

        except PackageNotFoundError:
            pass

        # When running from source code
        pyproject = (
            Path(__file__).parent.parent
            / "pyproject.toml"
        )

        with open(pyproject, "rb") as f:
            project = tomllib.load(f)

        return project["project"]["version"]

    @staticmethod
    def name():

        pyproject = (
            Path(__file__).parent.parent
            / "pyproject.toml"
        )

        with open(pyproject, "rb") as f:
            project = tomllib.load(f)

        return project["project"]["name"]