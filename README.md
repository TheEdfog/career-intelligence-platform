# Career Intelligence Platform

This FastAPI application compares a candidate profile with a vacancy. It extracts requirements, shows the evidence behind the match score and prepares a vacancy-specific resume and cover letter.

I originally built the idea as an academic project. This repository is the version I maintain: the application is packaged, tested and runnable without an external AI service.

## Main flow

```text
candidate profile + vacancy text
              |
              v
     normalized requirements
              |
              v
 evidence-based matching and skill gaps
              |
              v
 tailored resume and cover letter
```

Profiles, skills, vacancies, normalized requirements and generated documents are stored separately in PostgreSQL. This makes it possible to analyze several vacancies without copying the candidate profile.

The deterministic path handles parsing, matching and document generation locally. A DeepSeek-compatible API can be enabled for writing and parsing assistance, but it is not required.

## Match score

Each requirement receives an evidence score from exact skills, related skills and mentions in the profile. Mandatory requirements carry more weight in the final result:

```text
total_match = 0.75 * must_have_match + 0.25 * nice_to_have_match
```

The interface shows the supporting evidence rather than only displaying a percentage.

## Stack

Python 3.12, FastAPI, Jinja2, PostgreSQL 16, SQLAlchemy 2, Alembic, Pydantic, Pytest, Ruff, Docker Compose and GitHub Actions.

## Run with Docker

```bash
cp .env.example .env
docker compose up --build
```

Open <http://localhost:8000>. No LLM key is needed for the main workflow. For anything beyond local development, change `SECRET_KEY` and `POSTGRES_PASSWORD` in `.env`.

Stop the stack with `docker compose down`. Add `-v` only if you also want to remove the local database and generated documents.

## Run locally

```bash
python -m venv .venv
python -m pip install -r requirements-dev.txt
python -m uvicorn apps.web.main:app --reload
```

Copy `.env.example` to `.env` and set `DATABASE_URL` for the local PostgreSQL instance before starting the application.

## Checks

```bash
ruff check .
ruff format --check .
pytest
python -m compileall apps core
docker compose config -q
```

The tests cover routes, authentication boundaries, vacancy parsing, matching, recommendations, profile handling, HH integration boundaries and document fallbacks. Network and LLM calls are replaced with controlled test doubles.

## Repository layout

```text
apps/api/       database models, schemas and repositories
apps/web/       routes, services, templates and static files
config/         safe development defaults
core/           configuration, security and shared utilities
docs/           architecture diagrams
storage/        ignored runtime data
tests/          unit and web-layer tests
```

## Limits

- The score helps organize evidence; it is not a hiring decision.
- Related-skill mappings are explicit heuristics and need calibration for a particular role.
- Generated text should be reviewed before it is sent.
- A production deployment would also need managed secrets, HTTPS, rate limiting and a background queue for expensive jobs.

Licensed under GPL-3.0. See [LICENSE](LICENSE).
