import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from api.models import Url


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def test_url_create(api_client):
    payload = {"url": "https://example.com"}

    response = api_client.post(reverse("api:url-create"), payload)

    assert response.status_code == 201
    assert response.json()["url"] == "https://example.com"
    assert Url.objects.filter(url="https://example.com").exists()
