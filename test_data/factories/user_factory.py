from faker import Faker
import random

from schemas.request.createUserRequestSchema import CreateUserRequestSchema

faker = Faker()

class UserFactory:

    @staticmethod
    def build(**overrides):
        payload = {
            "first_name": faker.first_name(),
            "last_name": faker.last_name(),
            "email": faker.email(),
            "age": random.randint(18, 65),
            "phone": faker.phone_number(),
            "gender": random.choice(["Male", "Female"]),
            "address": {
                "street": faker.street_address(),
                "city": faker.city(),
                "state": faker.state(),
                "country": faker.country(),
                "zip_code": faker.postcode(),
            },
            "is_active": True,
            "role": random.choice(["Admin", "Manager", "User"]),
        }

        payload.update(overrides)

        return CreateUserRequestSchema(**payload)