# Schemas: Request and Response Validation

Schemas define the public shape of API data. Pydantic validates incoming data
and controls which fields are returned to clients.

## Why schemas are separate from models

A database model answers, “How is this stored?” A schema answers, “What may the
client send or receive?” Those answers are often different. For example, a
client should never send an auto-generated database ID.

## The three common schemas

[`task.py`](task.py) demonstrates this pattern:

- `TaskCreate`: required and optional fields for `POST`.
- `TaskUpdate`: optional fields for `PATCH`.
- `TaskRead`: fields included in API responses.

```python
class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr


class UserUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: EmailStr
```

`from_attributes=True` allows Pydantic to build a response from an SQLAlchemy
object. `Field` constraints become both runtime validation and OpenAPI docs.

## PATCH and `exclude_unset`

All update fields are optional because `PATCH` changes only fields sent by the
client. The repository uses `model_dump(exclude_unset=True)` so an omitted field
is not accidentally replaced by `None`.

## What belongs here

- Input validation and limits.
- Request and response field definitions.
- Serialization rules and examples.

Database queries and HTTP routing do not belong here.

Next: read [`../repositories/README.md`](../repositories/README.md).
