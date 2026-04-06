from django.urls import path

from .views import UrlListCreateView, UrlPingErrorView, UrlPingListView

app_name = "api"

urlpatterns = [
    path("urls/", UrlListCreateView.as_view(), name="url-list-create"),
    path("url-pings/", UrlPingListView.as_view(), name="url-ping-list"),
    path("url-ping/<int:pk>/error/", UrlPingErrorView.as_view(), name="url-ping-error"),
]
