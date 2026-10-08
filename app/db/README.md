# Database: Engine, Base, and Sessions

[`database.py`](database.py) contains the shared SQLAlchemy infrastructure.

## Engine

The engine manages connections to the configured database. `get_engine()` is
cached, so the application does not create a new connection pool per request.

```python
engine = get_engine("sqlite:///./tasks.db")
```

SQLite is ideal for this learning project because it needs no database server.
Production deployments commonly use PostgreSQL, but the surrounding layers can
remain nearly unchanged.

## Base

Every SQLAlchemy model inherits from `Base`. SQLAlchemy stores table metadata
on this shared class.

## Session

A session represents one unit of database work. `get_db()` yields a session to
FastAPI and closes it when the request ends—even if the request fails.

```text
Request begins -> open session -> query/commit -> close session -> request ends
```

Never keep a request session in a global variable.

## Table creation and migrations

`Base.metadata.create_all()` is intentionally used here to reduce setup work.
It creates missing tables, but it cannot safely evolve existing tables. Real
production projects normally use Alembic migrations for schema changes.

Next: read [`../core/README.md`](../core/README.md).
