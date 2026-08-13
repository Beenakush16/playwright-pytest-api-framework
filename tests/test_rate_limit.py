import time

import allure
import pytest



@pytest.mark.rate_limit
@pytest.mark.serial
@allure.feature("Rate Limiting")
class TestRateLimit:

    @pytest.mark.parametrize(
        "endpoint, expected_status",
        [
            ("GET /users", 200),
        ]
    )
    @allure.title("Validate API rate limiting")
    def test_api_rate_limit(
        self,
        endpoint,
        expected_status,
        user_api,
        config
    ):

        limit = config.get_max_requests(endpoint)

        for _ in range(limit):

            response = self._execute_request(
                endpoint,
                user_api,
            )

            assert response.status == expected_status

        response = self._execute_request(
            endpoint,
            user_api,
        )

        assert response.status == 429
        assert response.json()["message"] == "Rate limit exceeded."
        

    @pytest.mark.parametrize(
        "endpoint, expected_status",
        [
            ("GET /users", 200),
        ]
    )
    @allure.title("Validate API succeeds after rate limit window expires")
    def test_rate_limit_window_reset(
        self,
        endpoint,
        expected_status,
        user_api,
        config
    ):

        window = config.get_window_seconds(endpoint)
        limit = config.get_max_requests(endpoint)

        for _ in range(limit):

            response = self._execute_request(
                endpoint,
                user_api,
            )

            assert response.status == expected_status

        response = self._execute_request(
            endpoint,
            user_api,
        )

        assert response.status == 429

        time.sleep(window + 1)

        response = self._execute_request(
            endpoint,
            user_api,
        )

        assert response.status == expected_status

    @staticmethod
    def _execute_request(
        endpoint,
        user_api,
    ):

        if endpoint == "GET /users":
            return user_api.get_users()

        raise ValueError(f"Unsupported endpoint: {endpoint}")