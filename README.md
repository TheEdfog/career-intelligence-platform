# Career Intelligence Platform

A data-centric FastAPI application that turns a candidate profile and a vacancy into explainable fit scores, skill-gap recommendations, and tailored application documents.

The project demonstrates more than an LLM wrapper: vacancy text is normalized into structured requirements, candidate evidence is matched deterministically, results are persisted in PostgreSQL, and document generation remains usable when no external AI provider is configured.

## What it does

- manages authenticated candidate profiles and multiple vacancies;
- ingests vacancy text directly or retrieves supported public vacancy URLs;
- extracts normalized `must-have` and `nice-to-have` requirements;
- calculates explainable match scores with evidence for every requirement;
- separates resume improvements from genuine learning gaps;
- generates vacancy-specific resumes and cover letters;
- exports LaTeX and, when a TeX engine is available, PDF;
- optionally enriches parsing and writing through a DeepSeek-compatible API;
- keeps a deterministic fallback path for local development and tests.

## Architecture

```mermaid
flowchart LR
    U[Candidate] --> W[FastAPI + Jinja web app]
    V[Vacancy text or URL] --> W
    W --> P[Vacancy parser]
    P --> R[Normalized requirements]
    R --> M[Explainable matching engine]
    C[Candidate profile and skills] --> M
    M --> D[Recommendations and documents]
    W <--> DB[(PostgreSQL)]
    P -. optional .-> L[LLM provider]
    D -. optional .-> L
```

The relational model separates users, profiles, normalized skills, vacancies, vacancy requirements, generated resumes, and cover letters. This allows multiple vacancy analyses without duplicating the candidate profile.

![Entity relationship diagram](docs/assets/erd_3nf.png)

## Explainable scoring

Each vacancy requirement receives an evidence score based on exact skills, related skills, occurrences in profile text, and contextual evidence:

```text
evidence = min(
    1,
    0.65 * exact_skill_match
    + 0.35 * related_skill_match
    + 0.25 * min(text_hits / 3, 1)
    + 0.10 * context_score
)
```

The final score weights mandatory requirements more heavily:

```text
total_match = 0.75 * must_have_match + 0.25 * nice_to_have_match
```

The UI exposes the underlying evidence instead of presenting an unexplained percentage.

## Technology

| Area | Tools |
|---|---|
| Application | Python 3.12, FastAPI, Jinja2, Pydantic |
| Data layer | PostgreSQL 16, SQLAlchemy 2, Alembic |
| Security | JWT cookie sessions, Passlib/bcrypt |
| Integrations | vacancy APIs/pages, optional DeepSeek-compatible API |
| Documents | LaTeX with graceful text fallback |
| Quality | Pytest, Ruff, GitHub Actions |
| Delivery | Docker, Docker Compose, health checks |

## Quick start with Docker

No LLM key is required for the core matching flow.

```bash
cp .env.example .env
docker compose up --build
```

Open <http://localhost:8000>. PostgreSQL is reachable only inside the Compose network and is not exposed on the host.

For anything beyond local development, replace `SECRET_KEY` and `POSTGRES_PASSWORD` in `.env`.

Stop the stack with:

```bash
docker compose down
```

Add `-v` only when you intentionally want to remove local database and generated-document volumes.

## Local development

Create a virtual environment and install the development dependencies:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows PowerShell: .\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
```

Copy `.env.example` to `.env`, then point `DATABASE_URL` to your local development database:

```text
DATABASE_URL=postgresql+psycopg://career:career_dev_password@localhost:5432/career_intelligence
```

Run the app:

```bash
python -m uvicorn apps.web.main:app --reload
```

## Quality checks

```bash
ruff check .
ruff format --check .
pytest
python -m compileall apps core
docker compose config -q
```

The test suite covers routing, matching, vacancy parsing, recommendations, profile handling, HH integration boundaries, resume output, and deterministic document fallbacks. Network and LLM calls are replaced with controlled test doubles.

## Configuration

Defaults live in `config/app_config.toml`; environment variables take precedence. Important variables are documented in `.env.example`.

| Variable | Purpose |
|---|---|
| `DATABASE_URL` | SQLAlchemy PostgreSQL connection string |
| `SECRET_KEY` | JWT signing secret |
| `DEEPSEEK_API_KEY` | optional LLM provider key |
| `LLM_MODEL` | optional provider model name |
| `MAX_UPLOAD_SIZE_MB` | attachment size limit |
| `LATEX_ENGINE` | `xelatex` or `pdflatex` |

Do not commit `.env`, generated resumes, uploaded attachments, or vacancy source texts. They are excluded by `.gitignore` and `.dockerignore`.

## Repository layout

```text
apps/
  api/                  # models, schemas, repositories, DB setup
  web/                  # routes, services, templates, static assets
config/                 # safe development defaults
core/                   # configuration, security, shared utilities
docs/                   # diagrams and Postman smoke collection
storage/                # runtime data; contents are ignored
tests/                  # unit and web-layer tests
.github/workflows/      # automated quality gate
```

## Design boundaries

- Match scores are decision support, not hiring decisions.
- Related-skill mappings are explicit heuristics and should be calibrated for a target domain.
- LLM output is optional and must be reviewed by a human before use.
- Production deployment should use managed secrets, HTTPS, real migrations, rate limiting, and a background queue for expensive document jobs.

## Provenance

This is the canonical maintained portfolio edition of my academic prototype. Earlier snapshots were shared with classmates and may still exist under other GitHub accounts. This edition has its own packaging, security defaults, automated checks, containerized application, and documentation.

## License

GNU General Public License v3.0. See [LICENSE](LICENSE).
