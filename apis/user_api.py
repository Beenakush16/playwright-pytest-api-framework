from client.api_client import APIClient
from schemas.request.createUserRequestSchema import CreateUserRequestSchema


class UserAPI():

    def __init__(self, api_client: APIClient):
        self.client = api_client

    def get_users(self, **kwargs):
        return self.client.get("/users", **kwargs)
       #return self.client.get("/api/users", **kwargs)

    def get_user(self, user_id, **kwargs):
        return self.client.get(f"/api/users/{user_id}", **kwargs)

    def create_user(self, data: CreateUserRequestSchema, **kwargs):
        return self.client.post("/users", data=data.model_dump(mode="json"), **kwargs)
        #return self.client.post("/api/users", data=data, **kwargs)

    def update_user(self, user_id, data, **kwargs):
        return self.client.put(f"/api/users/{user_id}", data=data, **kwargs)

    def delete_user(self, user_id, **kwargs):
        return self.client.delete(f"/api/users/{user_id}", **kwargs)