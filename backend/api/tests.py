import pytest
from api.models import Url, UrlCheck
from django.urls import reverse
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def test_url_list_returns_urls_in_descending_created_order(api_client):
    older = Url.objects.create(url="https://older.example.com")
    newer = Url.objects.create(url="https://newer.example.com")

    response = api_client.get(reverse("api:url-list-create"))

    assert response.status_code == 200
    assert [item["id"] for item in response.json()] == [newer.id, older.id]


@pytest.mark.django_db
def test_url_create_persists_new_url_and_returns_serialized_data(api_client):
    payload = {"url": "https://created.example.com"}

    response = api_client.post(reverse("api:url-list-create"), payload, format="json")

    assert response.status_code == 201
    assert Url.objects.filter(url=payload["url"]).exists()
    assert response.json()["url"] == payload["url"]
    assert "id" in response.json()
    assert "created_at" in response.json()


@pytest.mark.django_db
def test_url_create_rejects_invalid_url(api_client):
    response = api_client.post(
        reverse("api:url-list-create"),
        {"url": "not-a-valid-url"},
        format="json",
    )

    assert response.status_code == 400
    assert "url" in response.json()


@pytest.mark.django_db
def test_url_check_list_returns_checks_in_descending_checked_order(api_client):
    url = Url.objects.create(url="https://checks.example.com")
    older = UrlCheck.objects.create(url=url, status_code=200)
    newer = UrlCheck.objects.create(url=url, status_code=503)

    response = api_client.get(reverse("api:url-check-list"))

    assert response.status_code == 200
    body = response.json()
    assert [item["id"] for item in body] == [newer.id, older.id]
    assert body[0]["url"] == url.id
    assert body[0]["status_code"] == 503
    assert "checked_at" in body[0]
