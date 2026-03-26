from django.urls import path
from .views import UrlCheckListView, UrlListCreateView

app_name = "api"

urlpatterns = [
    path("urls/", UrlListCreateView.as_view(), name="url-list-create"),
    path("url-checks/", UrlCheckListView.as_view(), name="url-check-list"),
]
