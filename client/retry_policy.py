from typing import Optional


class RetryPolicy:

    DEFAULT_RETRY_STATUS_CODES = {
        500,
        502,
        503,
        504
    }

    def __init__(self, config):

        retry_config = config.retry

        self.enabled = retry_config.get("enable", False)

        self.max_attempts = retry_config.get(
            "max_attempts",
            1
        )

        self.delay = retry_config.get(
            "delay",
            0
        )

        self.retry_status_codes = (
            self.DEFAULT_RETRY_STATUS_CODES
        )

    def should_retry(
        self,
        attempt: int,
        response=None,
        exception: Optional[Exception] = None
    ) -> bool:
        
        """
        Returns True if another retry should be attempted.
        """

        # Retry disabled
        if not self.enabled:
            return False

        # Max attempts reached
        if attempt >= self.max_attempts:
            return False

        # Network/Playwright exception
        if exception is not None:
            return True

        # HTTP response based retry
        if response is not None:
            return response.status in self.retry_status_codes

        return False