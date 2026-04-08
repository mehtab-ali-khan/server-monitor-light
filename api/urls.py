from django.urls import path

from api.views import UrlCreateView, UrlPingErrorView, UrlPingListView

app_name = "api"

urlpatterns = [
    path("url-create/", UrlCreateView.as_view(), name="url-create"),
    path("url-pings/", UrlPingListView.as_view(), name="url-ping-list"),
    path("url-ping/<int:pk>/error/", UrlPingErrorView.as_view(), name="url-ping-error"),
]
