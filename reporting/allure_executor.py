import json
import os
from pathlib import Path


class AllureExecutor:

    @staticmethod
    def write():

        results_dir = Path("allure-results")
        results_dir.mkdir(exist_ok=True)

        executor = {
            "reportName": "Playwright API Automation Report",
            "name": "Jenkins",
            "type": "jenkins",
            "url": os.getenv("JENKINS_URL", ""),
            "buildOrder": int(os.getenv("BUILD_NUMBER", "0")),
            "buildName": os.getenv("JOB_NAME", ""),
            "buildUrl": os.getenv("BUILD_URL", "")
        }

        with open(results_dir / "executor.json", "w") as f:
            json.dump(executor, f, indent=4)