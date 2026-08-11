import json
import allure


class AllureManager:

    @staticmethod
    def attach_request(
        method,
        endpoint,
        headers=None,
        params=None,
        body=None
    ):
        """
        Attach complete request information to Allure.
        """

        request_data = {
            "Method": method,
            "Endpoint": endpoint,
            "Headers": headers or {},
            "Query Parameters": params or {},
            "Body": body or {}
        }

        allure.attach(
            json.dumps(
                request_data,
                indent=4,
                default=str
            ),
            name="01_Request",
            attachment_type=allure.attachment_type.JSON
        )

    @staticmethod
    def attach_response(
        response,
        elapsed_time
    ):
        """
        Attach response body.
        """

        try:
            response_data = {
                "Status Code": response.status,
                "Headers": dict(response.headers),
                "Body": response.json()
            }
        except Exception:
            response_data = {
                "Status Code": response.status,
                "Headers": dict(response.headers),
                "Body": response.text()
            }

        allure.attach(
            json.dumps(
                response_data,
                indent=4,
                default=str
            ),
            name="02_Response",
            attachment_type=allure.attachment_type.JSON
        )

        allure.attach(
            f"{response.status} ({elapsed_time:.2f} ms)",
            name="03_Status_&_Response_Time",
            attachment_type=allure.attachment_type.TEXT
        )

    @staticmethod
    def attach_retry(
        attempt,
        max_attempts
    ):
        allure.attach(
            f"Retry Attempt : {attempt}/{max_attempts}",
            name=f"Retry_{attempt}",
            attachment_type=allure.attachment_type.TEXT
        )

    @staticmethod
    def attach_exception(exception):

        allure.attach(
            str(exception),
            name="04_Exception",
            attachment_type=allure.attachment_type.TEXT
        )

    @staticmethod
    def attach_text(name, text):

        allure.attach(
            str(text),
            name=name,
            attachment_type=allure.attachment_type.TEXT
        )

    @staticmethod
    def attach_json(name, data):

        allure.attach(
            json.dumps(
                data,
                indent=4,
                default=str
            ),
            name=name,
            attachment_type=allure.attachment_type.JSON
        )