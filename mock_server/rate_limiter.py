import re
from collections import defaultdict, deque
from datetime import datetime, timedelta


class RateLimiter:

    def __init__(self, config):

        self.enabled = config["enabled"]

        self.default = config["default"]

        self.endpoint_config = config.get(
            "endpoints",
            {}
        )

        self.requests = defaultdict(deque)

    def allow_request(
        self,
        method,
        path
    ):

        if not self.enabled:
            return True, 0

        endpoint = self.normalize_endpoint(
            method,
            path
        )

        endpoint_limit = self.endpoint_config.get(
            endpoint,
            self.default
        )

        max_requests = endpoint_limit["max_requests"]

        window_seconds = endpoint_limit["window_seconds"]

        history = self.requests[endpoint]

        now = datetime.now()

        window = timedelta(
            seconds=window_seconds
        )

        while (
            history
            and now - history[0] > window
        ):
            history.popleft()

        if len(history) >= max_requests:

            retry_after = (
                window_seconds
                - int(
                    (
                        now - history[0]
                    ).total_seconds()
                )
            )

            return False, retry_after

        history.append(now)

        return True, 0

    @staticmethod
    def normalize_endpoint(
        method,
        path
    ):

        path = re.sub(
            r"/\d+",
            "/<id>",
            path
        )

        return f"{method} {path}"

    def clear(self):
        self.requests.clear()