from rest_framework import serializers

from .models import Url, UrlCheck


class UrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = Url
        fields = ["id", "url", "created_at"]
        read_only_fields = ["id", "created_at"]


class UrlCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = UrlCheck
        fields = ["id", "url", "status_code", "checked_at"]
        read_only_fields = ["id", "checked_at"]
