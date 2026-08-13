import pytest
from playwright.sync_api import sync_playwright
from apis.user_api import UserAPI
from client.api_client import APIClient
from config.config import Config
from client.request_logger import RequestLogger
import subprocess
from config.logger import logger
from reporting.allure_environment import AllureEnvironment
from reporting.allure_executor import AllureExecutor

def pytest_addoption(parser):
    parser.addoption(
        "--env", action="store", default="qa", help="Environment to run tests against (qa, prod)"
    )

    parser.addoption(
        "--open-allure",
        action="store_true",
        default=False,
        dest="open_allure",
        help="Generate and open Allure report"
    )

@pytest.fixture(scope="session")
def environment(request):
    return request.config.getoption("--env")

@pytest.fixture(scope="session")
def config(environment):
    return Config(environment)

@pytest.fixture(scope="session")
def playwright():
    with sync_playwright() as p:
        yield p

@pytest.fixture(scope="session")
def api_request_context(playwright, config):

    request_context = playwright.request.new_context(
        base_url=config.base_url,
        timeout=config.timeout,
        ignore_https_errors=not config.verify_ssl
    )

    yield request_context

    request_context.dispose()

@pytest.fixture(scope="session")
def request_logger():

    return RequestLogger()

@pytest.fixture(scope="session")
def api_client(api_request_context, config, request_logger):
    return APIClient(api_request_context, config, request_logger)

"""playwright → create the Playwright runtime.
api_request_context → create the HTTP client.
api_client → wrap the HTTP client with your framework's functionality."""

@pytest.fixture(scope="session")
def user_api(api_client):
    return UserAPI(api_client)

def pytest_sessionstart(session):

    env = session.config.getoption("env")

    config = Config(env)

    AllureEnvironment.write(
        environment=env,
        base_url=config.base_url
    )
    AllureExecutor.write()

def pytest_sessionfinish(session, exitstatus):

    if not session.config.getoption("open_allure"):
        return

    try:
        subprocess.run(
            [
                "allure",
                "generate",
                "allure-results",
                "--clean",
                "-o",
                "allure-report"
            ],
            check=True
        )

        subprocess.run(
            [
                "allure",
                "open",
                "allure-report"
            ],
            check=True
        )

    except FileNotFoundError:
        logger.error(
            "Allure CLI is not installed. "
            "Install it using: brew install allure"
        )

    except subprocess.CalledProcessError as ex:
        logger.error(
            "Failed to generate/open Allure report: {}",
            ex
        )

@pytest.fixture(autouse=True)

def reset_rate_limit(api_client):

    api_client.post("/test/reset-rate-limit")

    yield