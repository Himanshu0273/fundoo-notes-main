import pytest
from faker import Faker

faker = Faker()


@pytest.fixture
def user_payload():
    return {
        "username": faker.user_name(),
        "email": "test@gm.com",
        "password": "Test@12345",
        "dob": faker.date_of_birth(minimum_age=18, maximum_age=30).isoformat(),
        "gender": "male",
    }
