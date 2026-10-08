# FastAPI Task CRUD

A beginner-friendly but production-inspired CRUD API using FastAPI, Pydantic,
SQLAlchemy, and SQLite. Code documentation is in English, as requested.

## Architecture

```text
app/
├── api/             # HTTP routes and dependency wiring
├── core/            # Application configuration
├── db/              # Engine, sessions, SQLAlchemy base
├── models/          # Database table mappings
├── repositories/    # Database queries only
├── schemas/         # Request/response validation
├── services/        # Business rules and use cases
└── main.py          # Application factory
tests/               # Isolated API/database tests
main.py              # Uvicorn entry point
```

Think of a request as a pipeline:

```text
Client -> Route -> Service -> Repository -> Database
       <- JSON  <- Model   <- ORM object <-
```

- **Route** understands HTTP: URL, status code, request, and response.
- **Service** understands business rules and use cases.
- **Repository** understands database queries.
- **Schema** validates data entering and leaving the API.
- **Model** describes how data is stored.

It has more files than putting everything in `main.py`, but each file has one
reason to change. That becomes valuable as an application grows.

## Setup (PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
uvicorn main:app --reload
```

Then open Swagger UI at <http://127.0.0.1:8000/docs>, ReDoc at
<http://127.0.0.1:8000/redoc>, or the health endpoint at
<http://127.0.0.1:8000/health>. SQLite creates `tasks.db` automatically.

## Endpoints

| Method | Path | Purpose | Success |
|---|---|---|---|
| POST | `/api/v1/tasks` | Create | `201` |
| GET | `/api/v1/tasks` | List (supports `offset` and `limit`) | `200` |
| GET | `/api/v1/tasks/{id}` | Read one | `200` |
| PATCH | `/api/v1/tasks/{id}` | Partially update | `200` |
| DELETE | `/api/v1/tasks/{id}` | Delete | `204` |

Example request:

```powershell
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/api/v1/tasks `
  -ContentType "application/json" `
  -Body '{"title":"Learn FastAPI","description":"Build CRUD"}'
```

## Tests

```powershell
pytest -q
```

Every test gets a separate temporary SQLite database, so tests never modify
development data. They test the public HTTP behavior and real repository code.

## Suggested learning order

Each important folder contains its own learning guide:

1. [`app/models/README.md`](app/models/README.md) — database table structure.
2. [`app/schemas/README.md`](app/schemas/README.md) — request and response validation.
3. [`app/repositories/README.md`](app/repositories/README.md) — database operations.
4. [`app/services/README.md`](app/services/README.md) — business rules.
5. [`app/api/README.md`](app/api/README.md) — dependencies, routes, and routers.
6. [`app/db/README.md`](app/db/README.md) — engine and database sessions.
7. [`app/core/README.md`](app/core/README.md) — application configuration.
8. [`tests/README.md`](tests/README.md) — testing strategy and examples.

For your first reading, follow that order to understand how an API is built.
Afterward, read it in reverse order—from the route to the model—to understand
how an incoming HTTP request travels through the running application.

## Checklist for adding a new resource

For a new resource such as `User`, use this sequence:

```text
1. app/models/user.py             Define the database table
2. app/schemas/user.py            Define input/output validation
3. app/repositories/user.py       Write database operations
4. app/services/user.py           Add business rules
5. app/api/dependencies.py        Wire repository and service together
6. app/api/routes/users.py        Define HTTP endpoints
7. app/api/router.py              Register the new router
8. tests/test_users.py            Prove the behavior works
```

For a larger production system, add Alembic migrations, structured logging,
authentication, and CI. They are omitted so this learning project stays focused.
