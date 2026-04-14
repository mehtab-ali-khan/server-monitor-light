from django.db.models import OuterRef, Subquery
from rest_framework import generics, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from api.models import Url, UrlPing
from api.serializers import UrlPingSerializer, UrlSerializer
from api.utils import get_error_url


class StandardPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class UrlCreateView(generics.CreateAPIView):
    queryset = Url.objects.all()
    serializer_class = UrlSerializer


class UrlPingListView(generics.ListAPIView):
    serializer_class = UrlPingSerializer
    pagination_class = StandardPagination

    def get_queryset(self):
        latest = (
            UrlPing.objects.filter(url=OuterRef("url"))
            .order_by("-time")
            .values("time")[:1]
        )

        return (
            UrlPing.objects.filter(time=Subquery(latest))
            .select_related("url")
            .order_by("-url_id")
        )


class UrlPingErrorView(generics.RetrieveAPIView):
    queryset = UrlPing.objects.all()

    def retrieve(self, request, *args, **kwargs):
        ping = self.get_object()

        if not ping.s3_key:
            return Response(
                {"error": "No snapshot for this ping"}, status=status.HTTP_404_NOT_FOUND
            )

        url = get_error_url(ping.s3_key)
        return Response({"snapshot_url": url})
