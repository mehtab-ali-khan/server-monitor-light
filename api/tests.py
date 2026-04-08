import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from api.models import Url


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def test_url_list_returns_urls_in_descending_created_order(api_client):
    older = Url.objects.create(url="https://older.example.com")
    newer = Url.objects.create(url="https://newer.example.com")

    response = api_client.get(reverse("api:url-create"))

    assert response.status_code == 200
    assert [item["id"] for item in response.json()] == [newer.id, older.id]
