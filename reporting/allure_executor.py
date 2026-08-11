import json
import os
from pathlib import Path


class AllureExecutor:

    @staticmethod
    def write():

        allure_results = Path("allure-results")
        allure_results.mkdir(exist_ok=True)

        executor = {

            "name": "Jenkins",

            "type": "jenkins",

            "url": os.getenv(
                "JENKINS_URL",
                "http://localhost:8080"
            ),

            "buildName": os.getenv(
                "JOB_NAME",
                ""
            ),

            "buildOrder": int(
                os.getenv(
                    "BUILD_NUMBER",
                    "0"
                )
            ),

            "buildUrl": os.getenv(
                "BUILD_URL",
                ""
            ),

            "reportName": (
                "Playwright API Automation Report"
            )
        }

        with open(
            allure_results / "executor.json",
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                executor,
                file,
                indent=4
            )