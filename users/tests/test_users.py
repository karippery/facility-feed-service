
import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from facility_feed_service.common.choices import Userroles

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_user():
    def _create_user(**kwargs):
        return User.objects.create_user(**kwargs)
    return _create_user


@pytest.fixture
def create_superuser():
    def _create_superuser(**kwargs):
        return User.objects.create_superuser(**kwargs)
    return _create_superuser


@pytest.mark.django_db
def test_create_user(create_user):
    user = create_user(email='test@example.com', first_name='John', last_name='Raphy', password='password123', role=Userroles.ADMIN)
    assert user.email == 'test@example.com'
    assert user.first_name == 'John'
    assert user.last_name == 'Raphy'
    assert user.check_password('password123')
    assert not user.is_superuser
    assert not user.is_staff


@pytest.mark.django_db
def test_create_superuser(create_superuser):
    user = create_superuser(email='admin@example.com', first_name='Admin', last_name='User', password='adminpass')
    assert user.is_superuser
    assert user.is_staff
    assert user.role == Userroles.ADMIN


@pytest.mark.django_db
def test_user_list_api(api_client, create_user):
    create_user(email='test1@example.com', first_name='User1', last_name='Test', password='password123', role=Userroles.Customer)
    create_user(email='test2@example.com', first_name='User2', last_name='Test', password='password123', role=Userroles.Customer)
    response = api_client.get("/users/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED  # Requires authentication


@pytest.mark.django_db
def test_user_create_api(api_client):
    data = {
        "email": "newuser@example.com",
        "first_name": "New",
        "last_name": "User",
        "password": "newpassword",
        "role": Userroles.Customer,
    }
    response = api_client.post("/users/", data, format="json")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED  # Authentication required


@pytest.mark.django_db
def test_token_obtain(api_client, create_user):
    create_user(email='test@example.com', first_name='John', last_name='Raphy', password='password123', role=Userroles.ADMIN)
    data = {"email": "test@example.com", "password": "password123"}
    response = api_client.post("/users/token/", data, format="json")
    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data
    assert "refresh" in response.data
