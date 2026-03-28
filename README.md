# Url_App

## Pre-commit

Install pre-commit once on your machine:

```bash
pip install pre-commit
pre-commit install
```

Run all hooks manually at any time:

```bash
pre-commit run --all-files
```

Configured hooks:
- `trailing-whitespace`
- `end-of-file-fixer`
- `check-yaml`
- `check-added-large-files`
- `black`
- `isort`
- `ruff --fix`

## CI

GitHub Actions CI is defined in `.github/workflows/ci.yml`.

It does two things:
- runs `pre-commit` on all files
- runs `pytest` in the `backend` directory using `core.test_settings`

This means pull requests and pushes are checked with the same formatting, linting, and test flow every time.

## CD

GitHub Actions deploy is defined in `.github/workflows/deploy.yml`.

Deployment runs only when:
- the `CI` workflow finishes successfully
- the branch is `main`

The deploy job connects to your EC2 instance and runs:

```bash
cd <project-path>
git fetch origin
git checkout main
git pull origin main
cd backend
docker compose up -d --build
docker compose ps
```

This matches your current Docker Compose deployment style.

## Required GitHub Secrets

Add these in your GitHub repository settings under Actions secrets:
- `EC2_HOST`
- `EC2_USER`
- `EC2_SSH_KEY`
- `EC2_PROJECT_PATH`

Example `EC2_PROJECT_PATH`:

```text
/home/ubuntu/Url_App
```
