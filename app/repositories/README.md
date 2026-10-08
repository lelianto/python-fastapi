# Repositories: Database Operations

A repository is the only application layer that should perform normal database
queries. It receives a SQLAlchemy `Session` and returns ORM objects.

## Current example

[`task.py`](task.py) implements these operations:

- `create()` adds and commits a row.
- `list()` executes a paginated `SELECT`.
- `get()` retrieves one row by primary key.
- `update()` changes only submitted fields.
- `delete()` removes and commits a row.

```python
class UserRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_email(self, email: str) -> User | None:
        query = select(User).where(User.email == email)
        return self.session.scalar(query)
```

## Why commit and refresh?

`commit()` permanently saves a transaction. `refresh()` reloads database-made
values such as the generated ID before the object is returned.

## Repository boundary

The repository may know about SQLAlchemy, tables, and queries. It should not
know about FastAPI, `HTTPException`, JSON, or status code `404`. If the row does
not exist, it returns `None`; the service decides what that means.

## Common mistakes

- Placing business rules inside database queries.
- Forgetting to commit a create, update, or delete.
- Returning raw tuples when the service expects ORM objects.
- Creating a new session manually instead of using dependency injection.

Next: read [`../services/README.md`](../services/README.md).
