from rest_framework import generics
from .models import Url, UrlCheck
from .serializers import UrlCheckSerializer, UrlSerializer


class UrlListCreateView(generics.ListCreateAPIView):
    queryset = Url.objects.all().order_by("-created_at")
    serializer_class = UrlSerializer


class UrlCheckListView(generics.ListAPIView):
    queryset = UrlCheck.objects.select_related("url").order_by("-checked_at")
    serializer_class = UrlCheckSerializer
