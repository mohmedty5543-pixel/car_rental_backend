import pytest
from rest_framework.test import APIClient
from apps.users.models import User

@pytest.fixture
def api():
    return APIClient()

@pytest.fixture
def user(db):
    return User.objects.create_user(email='u@example.com', password='pw12345678',
                                    full_name='U')
