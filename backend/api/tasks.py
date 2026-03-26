import requests
from celery import shared_task
from .models import Url, UrlCheck


@shared_task
def check_all_urls():
    urls = Url.objects.all()

    for url_obj in urls:
        try:
            response = requests.get(url_obj.url, timeout=10)
            status_code = response.status_code
        except requests.RequestException:
            status_code = None

        UrlCheck.objects.create(
            url=url_obj,
            status_code=status_code,
        )

    return f"Checked {urls.count()} urls"
