from django.contrib import admin

from .models import Url, UrlPing


@admin.register(Url)
class UrlAdmin(admin.ModelAdmin):
    list_display = ["url", "created_at"]
    search_fields = ["url"]


@admin.register(UrlPing)
class UrlPingAdmin(admin.ModelAdmin):
    list_display = ["url", "status_code", "time", "error"]
    list_filter = ["status_code"]
    search_fields = ["url__url"]
