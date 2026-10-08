# Models: Database Tables

Models describe how application data is stored. In this project, models use
SQLAlchemy ORM, which maps a Python class to a database table.

## Current example

[`task.py`](task.py) contains `Task`. The class maps to the `tasks` table, and
each typed `mapped_column()` becomes a column.

```python
class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
```

An instance such as `Task(title="Learn FastAPI")` represents one row. Calling
`session.add(task)` and `session.commit()` persists that row.

## Creating a new model

For a `User` resource, create `app/models/user.py`:

```python
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.db.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
```

Then import it inside `create_db_and_tables()` in `app/db/database.py` so
SQLAlchemy knows that the table exists.

## What belongs here

- Table and column names.
- Database types and constraints.
- Relationships between tables.
- Database-level defaults.

HTTP status codes and request validation do not belong in a model.

## Common mistakes

- Forgetting to inherit from `Base`.
- Using a nullable column for data that must always exist.
- Forgetting `unique=True` for naturally unique fields such as email.
- Returning ORM models directly without a response schema.

Next: read [`../schemas/README.md`](../schemas/README.md).
