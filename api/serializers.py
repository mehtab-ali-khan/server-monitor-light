from rest_framework import serializers

from api.models import Url, UrlPing


class UrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = Url
        fields = ["id", "url", "created_at"]
        read_only_fields = ["id", "created_at"]


class UrlPingSerializer(serializers.ModelSerializer):
    url_string = serializers.CharField(source="url.url", read_only=True)
    has_error = serializers.SerializerMethodField()

    class Meta:
        model = UrlPing
        fields = ["id", "url_string", "status_code", "time", "has_error"]
        read_only_fields = ["id", "time"]

    def get_has_error(self, obj):
        return obj.s3_key is not None
