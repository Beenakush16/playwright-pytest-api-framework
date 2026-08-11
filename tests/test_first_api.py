from playwright.sync_api import sync_playwright
from test_data.factories.user_factory import UserFactory
from schemas.response.createUserResponseSchema import CreateUserResponseSchema
import allure


from conftest import user_api

@allure.title("Validate Get Users API")
def test_getUsers_api(user_api):
    response = user_api.get_users()
    assert response.status == 200

    data = response.json()
    print(data)

@allure.title("Validate Create User API")
@allure.severity(allure.severity_level.CRITICAL)
def test_create_user_api(user_api):
    payload = UserFactory.build()
    response = user_api.create_user(payload)
    validated_response = CreateUserResponseSchema.model_validate(response.json())
    assert validated_response.email == payload.email
    print(response.json())
    
"""
Test - verifies business behavior.
UserAPI - knows user-related endpoints and operations.
APIClient - knows how to send HTTP requests consistently.
APIRequestContext - actually communicates with the server."""