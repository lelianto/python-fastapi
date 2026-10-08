# API: Dependencies, Routes, and Routers

The API layer converts HTTP requests into service calls and converts results or
domain errors back into HTTP responses.

## Dependencies

[`dependencies.py`](dependencies.py) assembles objects for each request:

```text
SQLAlchemy Session -> TaskRepository -> TaskService -> Endpoint
```

FastAPI sees `Depends(get_task_service)`, calls the provider, and injects the
result into the endpoint. This keeps construction code out of routes and makes
dependencies replaceable during tests.

For a new resource, add its repository/service provider:

```python
def get_user_service(session: DatabaseSession) -> UserService:
    return UserService(UserRepository(session))


UserServiceDependency = Annotated[UserService, Depends(get_user_service)]
```

## Routes

[`routes/tasks.py`](routes/tasks.py) defines the HTTP contract. Each endpoint
chooses its method, URL, schemas, status code, and service method.

```python
@router.post("", response_model=UserRead, status_code=201)
def create_user(payload: UserCreate, service: UserServiceDependency) -> UserRead:
    return service.create(payload)
```

Use HTTP methods consistently:

| Method | Meaning | Typical success |
|---|---|---|
| POST | Create | `201 Created` |
| GET | Read | `200 OK` |
| PATCH | Partially update | `200 OK` |
| DELETE | Delete | `204 No Content` |

## Router registration

After creating `routes/users.py`, register it in [`router.py`](router.py):

```python
from app.api.routes.users import router as users_router

api_router.include_router(users_router)
```

Forgetting registration is a common reason a valid-looking endpoint returns
`404 Not Found`.

## Complete request flow

```text
POST /api/v1/tasks
  -> TaskCreate validates JSON
  -> endpoint calls TaskService
  -> service calls TaskRepository
  -> repository commits a Task model
  -> TaskRead serializes the result
  -> client receives JSON with status 201
```

Next: read [`../db/README.md`](../db/README.md).
