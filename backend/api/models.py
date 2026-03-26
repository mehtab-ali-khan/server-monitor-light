from django.db import models


class Url(models.Model):
    url = models.URLField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.url


class UrlCheck(models.Model):
    url = models.ForeignKey(Url, on_delete=models.CASCADE, related_name="checks")
    status_code = models.IntegerField(null=True, blank=True)
    checked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.url.url} — {self.status_code} at {self.checked_at}"
