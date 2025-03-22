from facility_feed_service.common.choices import Userroles
import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from feed_service.models import Facility
from users.models import User


@pytest.fixture
def authenticated_client(db):
    """Fixture to provide an authenticated test client."""
    client = APIClient()

    # Create a test user
    user = User.objects.create_user(
        email="testuser@example.com",
        first_name="Test",
        last_name="User",
        password="password123",
        role=Userroles.ADMIN
    )

    # Obtain an authentication token
    url = reverse('token_obtain_pair')
    response = client.post(url, {"email": user.email, "password": "password123"}, format="json")

    assert response.status_code == 200, f"Failed to obtain token: {response.data}"
    token = response.data["access"]

    # Set authorization header
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    return client


@pytest.mark.django_db
def test_facility_creation(authenticated_client):
    """Test creating a new facility."""
    url = reverse('facility-list-create')
    data = {
        "name": "Test Facility",
        "phone": "1234567890",
        "url": "http://example.com",
        "latitude": 12.345,
        "longitude": 67.890,
        "country": "Test Country",
        "locality": "Test Locality",
        "region": "Test Region",
        "postal_code": "12345",
        "street_address": "123 Test St.",
    }
    response = authenticated_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["name"] == "Test Facility"


@pytest.mark.django_db
def test_facility_list(authenticated_client):
    """Test retrieving a list of facilities."""
    Facility.objects.create(
        name="Test Facility 1", phone="1234567890", url="http://example1.com",
        latitude=12.345, longitude=67.890, country="Country 1", locality="Locality 1",
        region="Region 1", postal_code="12345", street_address="Street 1"
    )
    Facility.objects.create(
        name="Test Facility 2", phone="0987654321", url="http://example2.com",
        latitude=12.345, longitude=67.890, country="Country 2", locality="Locality 2",
        region="Region 2", postal_code="67890", street_address="Street 2"
    )

    url = reverse("facility-list-create")
    response = authenticated_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data["results"]) == 2


@pytest.mark.django_db
def test_facility_detail(authenticated_client):
    """Test retrieving a specific facility."""
    facility = Facility.objects.create(
        name="Test Facility",
        phone="1234567890",
        url="http://example.com",
        latitude=12.345,
        longitude=67.890,
        country="Test Country",
        locality="Test Locality",
        region="Test Region",
        postal_code="12345",
        street_address="123 Test St.",
    )
    url = reverse("facility-retrieve-update-destroy", kwargs={"pk": facility.pk})
    response = authenticated_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["name"] == facility.name
