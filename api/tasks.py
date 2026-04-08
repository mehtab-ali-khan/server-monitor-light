import requests
from celery import shared_task

from api.models import Url, UrlPing
from api.utils import upload_error


@shared_task
def check_all_urls():
    urls = Url.objects.all()

    for url_obj in urls:
        try:
            response = requests.get(url_obj.url, timeout=10)
            status_code = response.status_code
            error = None
            s3_key = None

            if not (200 <= status_code < 300):
                error = response.text
                s3_key = upload_error(response.text, url_obj.url)

            UrlPing.objects.create(
                url=url_obj, status_code=status_code, error=error, s3_key=s3_key
            )

        except Exception as e:
            UrlPing.objects.create(url=url_obj, status_code=0, error=e)
