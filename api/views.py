from django.db.models import OuterRef, Subquery
from rest_framework import generics, status
from rest_framework.response import Response

from .models import Url, UrlPing
from .serializers import UrlPingSerializer, UrlSerializer
from .utils import get_error_url


class UrlListCreateView(generics.ListCreateAPIView):
    queryset = Url.objects.all().order_by("-created_at")
    serializer_class = UrlSerializer


class UrlPingListView(generics.ListAPIView):
    serializer_class = UrlPingSerializer

    def get_queryset(self):
        latest = (
            UrlPing.objects.filter(url=OuterRef("url"))
            .order_by("-time")
            .values("time")[:1]
        )

        return (
            UrlPing.objects.filter(time=Subquery(latest))
            .select_related("url")
            .order_by("url_id")
        )


class UrlPingErrorView(generics.RetrieveAPIView):
    queryset = UrlPing.objects.all()

    def retrieve(self, request, *args, **kwargs):
        ping = self.get_object()

        if not ping.error:
            return Response(
                {"error": "No snapshot for this ping"}, status=status.HTTP_404_NOT_FOUND
            )

        url = get_error_url(ping.error)
        return Response({"snapshot_url": url})
