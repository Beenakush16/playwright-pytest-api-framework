import copy
import json
import traceback

from config.logger import logger
from reporting.allure_manager import AllureManager


class RequestLogger:

    SENSITIVE_KEYS = {
        "authorization",
        "password",
        "token",
        "access_token",
        "refresh_token",
        "secret",
        "api_key",
        "apikey",
        "x-api-key"
    }

    def log_request(
        self,
        method,
        endpoint,
        headers=None,
        params=None,
        data=None
    ):

        masked_headers = self.mask_sensitive_data(headers)
        masked_params = self.mask_sensitive_data(params)
        masked_data = self.mask_sensitive_data(data)

        logger.info("=" * 80)
        logger.info("REQUEST STARTED")
        logger.info("Method      : {}", method)
        logger.info("Endpoint    : {}", endpoint)

        if masked_params:
            logger.info(
                "Query Params:\n{}",
                json.dumps(masked_params, indent=4)
            )

        if masked_headers:
            logger.info(
                "Headers:\n{}",
                json.dumps(masked_headers, indent=4)
            )

        if masked_data:
            logger.info(
                "Request Body:\n{}",
                json.dumps(masked_data, indent=4)
            )

        # -----------------------------
        # Allure Attachment
        # -----------------------------
        AllureManager.attach_request(
            method=method,
            endpoint=endpoint,
            headers=masked_headers,
            params=masked_params,
            body=masked_data
        )

    def log_response(
        self,
        response,
        elapsed_time
    ):

        logger.info("REQUEST COMPLETED")
        logger.info("Status Code   : {}", response.status)
        logger.info("Response Time : {:.2f} ms", elapsed_time)

        try:
            logger.info(
                "Response Body:\n{}",
                json.dumps(
                    response.json(),
                    indent=4
                )
            )
        except Exception:
            logger.info(response.text())

        logger.info("=" * 80)

        # -----------------------------
        # Allure Attachment
        # -----------------------------
        AllureManager.attach_response(
            response=response,
            elapsed_time=elapsed_time
        )

    def log_exception(
        self,
        exception,
        elapsed_time
    ):

        logger.error("=" * 80)
        logger.error("REQUEST FAILED")
        logger.error("Elapsed Time  : {:.2f} ms", elapsed_time)
        logger.error(
            "Exception Type : {}",
            type(exception).__name__
        )
        logger.error("Message        : {}", str(exception))
        logger.error(traceback.format_exc())
        logger.error("=" * 80)

        # -----------------------------
        # Allure Attachment
        # -----------------------------
        AllureManager.attach_exception(exception)

    def mask_sensitive_data(self, data):

        if data is None:
            return None

        masked_data = copy.deepcopy(data)

        self._mask(masked_data)

        return masked_data

    def _mask(self, value):

        if isinstance(value, dict):

            for key, item in value.items():

                if key.lower() in self.SENSITIVE_KEYS:
                    value[key] = "********"
                else:
                    self._mask(item)

        elif isinstance(value, list):

            for item in value:
                self._mask(item)