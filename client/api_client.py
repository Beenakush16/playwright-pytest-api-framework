import time

from client.retry_policy import RetryPolicy
from client.timer import Timer
from client.request_result import RequestResult
from playwright.sync_api import APIRequestContext
from client.request_logger import RequestLogger




class APIClient:

    def __init__(self, request_context: APIRequestContext, config, request_logger: RequestLogger):
        self.request = request_context
        self.config = config
        self.request_logger = request_logger
        # No fixture required for now
        self.retry_policy = RetryPolicy(config)

    """**kwargs allows us to pass any optional parameters supported
    by Playwright without changing the method signature. Like headers, query parameters, timeout etc. This makes the APIClient class flexible and adaptable to different API endpoints and requirements."""
    def get(self, endpoint, **kwargs):
        return self._send("GET", endpoint, **kwargs)

    def post(self, endpoint, **kwargs):
        return self._send("POST", endpoint, **kwargs)

    def put(self, endpoint, **kwargs):
        return self._send("PUT", endpoint, **kwargs)

    def delete(self, endpoint, **kwargs):
        return self._send("DELETE", endpoint, **kwargs)

    def _send(self, method, endpoint, **kwargs):

        # Start with default headers from config
        headers = self._build_headers(kwargs.get("headers"))

        # IMPORTANT: send these headers
        kwargs["headers"] = headers

        self.request_logger.log_request(
            method=method,
            endpoint=endpoint,
            headers=headers,
            params=kwargs.get("params"),
            data=kwargs.get("data")
        )

        result = self._execute_request(
            method,
            endpoint,
            **kwargs
        )

        self.request_logger.log_response(
            response=result.response,
            elapsed_time=result.elapsed_time
        )

        return result.response

    def _execute_request(
        self,
        method,
        endpoint,
        **kwargs
    ):
        for attempt in range(1, self.retry_policy.max_attempts + 1):

            timer = Timer()

            try:

                with timer:
                    response = self._perform_request(
                        method,
                        endpoint,
                        **kwargs
                    )

                # Retry for retryable status codes
                if self.retry_policy.should_retry(
                    attempt=attempt,
                    response=response
                ):
                    time.sleep(self.retry_policy.delay)
                    continue
                return RequestResult(
                    response=response,
                    elapsed_time=timer.elapsed_ms
                )

            except Exception as ex:

                # Retry for network/playwright exceptions
                if self.retry_policy.should_retry(
                    attempt=attempt,
                    exception=ex
                ):
                    time.sleep(self.retry_policy.delay)
                    continue
                self.request_logger.log_exception(
                    exception=ex,
                    elapsed_time=timer.elapsed_ms
                )

                raise

    def _perform_request(
        self,
        method,
        endpoint,
        **kwargs
    ):

        return getattr(
            self.request,
            method.lower()
        )(
            endpoint,
            **kwargs
        )

    def _build_headers(
        self,
        request_headers=None
    ):

        headers = self.config.headers.copy()

        if request_headers:
            headers.update(request_headers)

        return headers