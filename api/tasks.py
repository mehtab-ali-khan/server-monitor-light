import requests
from celery import shared_task

from api.models import Url, UrlPing
from api.utils import upload_error

REQUEST_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
}


@shared_task
def check_all_urls():
    url_ids = list(Url.objects.values_list("id", flat=True))

    for url_id in url_ids:
        check_one_url.delay(url_id)


@shared_task
def check_one_url(url_id):
    try:
        url_obj = Url.objects.get(id=url_id)
    except Url.DoesNotExist:
        return

    try:
        response = requests.get(
            url_obj.url,
            timeout=5,
            headers=REQUEST_HEADERS,
        )

        error = None
        if not (200 <= response.status_code < 300):
            error = response.text

        ping = UrlPing.objects.create(
            url=url_obj,
            status_code=response.status_code,
            error=error,
        )

        if error:
            upload_error_snapshot.delay(ping.id)

    except Exception as e:
        UrlPing.objects.create(url=url_obj, status_code=0, error=str(e))


@shared_task
def upload_error_snapshot(ping_id):
    try:
        ping = UrlPing.objects.select_related("url").get(id=ping_id)
    except UrlPing.DoesNotExist:
        return

    if not ping.error:
        return

    if ping.s3_key:
        return

    s3_key = upload_error(ping.error, ping.url.url)

    ping.s3_key = s3_key
    ping.save(update_fields=["s3_key"])
