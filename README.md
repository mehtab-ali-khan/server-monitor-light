# URL App Backend

This repository is a Django + Django REST Framework backend for monitoring URLs. It stores submitted URLs, checks them on a schedule with Celery, records each result as a `UrlPing`, and keeps a retrievable S3 snapshot for non-2xx responses.

## What It Does

- Create URLs to monitor
- Run background health checks every minute
- Store each check result with status code and timestamp
- Save failing HTML responses to S3
- Return a presigned URL for a stored error snapshot

## Stack

- Django 5
- Django REST Framework
- PostgreSQL
- Redis
- Celery worker + Celery beat
- Boto3 for S3 uploads
- Docker / Docker Compose

## Project Structure

```text
core/
  settings.py      Django settings, DB, Celery, CORS
  urls.py          Root URL config
  celery.py        Celery app setup

api/
  models.py        Url and UrlPing models
  serializers.py   API serializers
  views.py         API endpoints
  tasks.py         Scheduled URL checking task
  utils.py         S3 upload and presigned URL helpers
  urls.py          App routes
  tests.py         API tests
```

## Architecture

The system has four main pieces:

1. Django API accepts URLs from clients and stores them in PostgreSQL.
2. Celery Beat triggers `check_all_urls` every 60 seconds.
3. Celery Worker sends HTTP requests to each saved URL and creates a `UrlPing` record.
4. If a response is not `2xx`, the response body is uploaded to S3 and can later be accessed through a presigned URL.

High-level flow:

```text
Client -> Django API -> PostgreSQL
                     -> Celery Beat -> Celery Worker -> External URL
                                                    -> PostgreSQL (UrlPing)
                                                    -> S3 (error snapshot)
```

## Data Model

### `Url`

- `url`: target URL to monitor
- `created_at`: timestamp when the URL was added

### `UrlPing`

- `url`: foreign key to `Url`
- `status_code`: HTTP status code from the latest check
- `time`: timestamp of the check
- `error`: response body or exception text for failures
- `s3_key`: S3 object key for stored error HTML

## Environment Variables

Create a `.env` file based on `.env.example`.

```env
# Django
SECRET_KEY=change-me
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
POSTGRES_DB=urlapp
POSTGRES_USER=urluser
POSTGRES_PASSWORD=strongpassword123
DB_HOST=db

# Celery / Redis
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0

# AWS
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_BUCKET_NAME=your-bucket
AWS_REGION=your-region
```

## Local Setup

### Option 1: Docker Compose

This is the easiest way to run the full stack.

1. Copy `.env.example` to `.env` and fill in the values.
2. Start the services:

```bash
docker compose up --build
```

Services started by `docker-compose.yml`:

- `backend` on `http://localhost:8000`
- `celery_worker`
- `celery_beat`
- `db` on port `5432`
- `redis` on port `6379`

### Option 2: Run Locally Without Docker

You will need PostgreSQL and Redis running locally first.

1. Create and activate a virtual environment
2. Install dependencies
3. Configure `.env`
4. Run migrations
5. Start Django, Celery worker, and Celery beat in separate terminals

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
celery -A core worker --loglevel=info
celery -A core beat --loglevel=info
```

## API

Base path:

```text
/api/
```

### 1. Create URL

`POST /api/url-create/`

Request:

```bash
curl -X POST http://localhost:8000/api/url-create/ \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com"}'
```

Response:

```json
{
  "id": 1,
  "url": "https://example.com",
  "created_at": "2026-04-08T10:15:00Z"
}
```

### 2. List Latest Ping for Each URL

`GET /api/url-pings/`

This endpoint returns the most recent `UrlPing` per saved URL.

Request:

```bash
curl http://localhost:8000/api/url-pings/
```

Response:

```json
[
  {
    "id": 14,
    "url_string": "https://example.com",
    "status_code": 200,
    "time": "2026-04-08T10:16:00Z",
    "has_error": false
  },
  {
    "id": 15,
    "url_string": "https://example.org",
    "status_code": 500,
    "time": "2026-04-08T10:16:00Z",
    "has_error": true
  }
]
```

### 3. Get Error Snapshot URL

`GET /api/url-ping/<id>/error/`

If a failing response snapshot was uploaded to S3, this returns a presigned URL.

Request:

```bash
curl http://localhost:8000/api/url-ping/15/error/
```

Response:

```json
{
  "snapshot_url": "https://your-bucket.s3.amazonaws.com/..."
}
```

If there is no snapshot:

```json
{
  "error": "No snapshot for this ping"
}
```

## Scheduled Task

The periodic task is defined in `core/settings.py`:

- Task: `api.tasks.check_all_urls`
- Schedule: every 60 seconds

For each stored URL, the task:

- sends a GET request with a 10-second timeout
- stores the returned status code
- uploads the response body to S3 for non-2xx responses
- creates a `UrlPing` record

## Seeding Test Data

The repo includes a management command to generate sample URLs:

```bash
python manage.py seed_urls
```

## Testing

Run tests with:

```bash
pytest
```

Note: tests use the Django database settings from `core/settings.py`, so your configured PostgreSQL instance must be reachable.

## Production Notes

The `prod/docker-compose.yml` setup adds:

- `gunicorn` for the Django app
- `nginx` as a reverse proxy
- persistent Docker volumes for Postgres and static/media files

