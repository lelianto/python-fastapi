# Services: Business Logic

Services describe application use cases. They coordinate repositories and
enforce rules without depending on HTTP.

## Current example

[`task.py`](task.py) delegates basic persistence to `TaskRepository` and turns a
missing row into `TaskNotFoundError`.

```python
class UserService:
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    def create(self, payload: UserCreate) -> User:
        if self.repository.get_by_email(payload.email):
            raise EmailAlreadyExistsError(payload.email)
        return self.repository.create(payload)
```

The rule “email must be unique” belongs here because it expresses application
behavior. A CLI command or background job could reuse this same service without
importing FastAPI.

## What belongs here

- Business validation and decisions.
- Coordinating multiple repositories.
- Domain-specific exceptions.
- Calculations and workflows.

Routes, status codes, and `HTTPException` do not belong here. A route translates
a domain exception such as `EmailAlreadyExistsError` into an HTTP response such
as `409 Conflict`.

## When a service looks too simple

For basic CRUD, a service may only call a repository. Keeping the layer is still
useful when you expect rules to grow. In a very small throwaway application, it
is also reasonable to omit this layer; architecture should serve the project.

Next: read [`../api/README.md`](../api/README.md).
