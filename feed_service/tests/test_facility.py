import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from feed_service.models import Facility


@pytest.fixture
def client():
    """Fixture to provide a DRF test client."""
    return APIClient()


@pytest.mark.django_db
def test_facility_creation(client):
    """Test creating a new facility."""
    url = reverse('facility-list-create')  # URL for the FacilityListCreateView
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
    response = client.post(url, data, format='json')  # POST request to create a facility
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['name'] == "Test Facility"


@pytest.mark.django_db
def test_facility_list(client):
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

    url = reverse('facility-list-create')  
    response = client.get(url)  

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data['results']) == 2  # Check the length of the 'results' key


@pytest.mark.django_db
def test_facility_detail(client):
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
    url = reverse('facility-retrieve-update-destroy', kwargs={'pk': facility.pk})  # URL for retrieving a facility
    response = client.get(url)  # GET request to fetch the facility details

    assert response.status_code == status.HTTP_200_OK
    assert response.data['name'] == facility.name


@pytest.mark.django_db
def test_generate_feed_command():
    """Test running the 'generate_feed' management command."""
    from django.core.management import call_command
    # Ensure the command runs successfully without errors
    result = call_command('generate_feed')
    assert result is None  # Check that the command runs without issues (returns None)