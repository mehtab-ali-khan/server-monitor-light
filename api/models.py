from django.db import models


class Url(models.Model):
    url = models.URLField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.url


class UrlPing(models.Model):
    url = models.ForeignKey(Url, on_delete=models.CASCADE, related_name="pings")
    status_code = models.IntegerField()
    time = models.DateTimeField(auto_now_add=True)
    error = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.url.url} — {self.status_code} at {self.time}"
