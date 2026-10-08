# Tests: Proving API Behavior

Tests provide fast feedback and document how the API should behave.

## Test setup

[`conftest.py`](conftest.py) provides the shared `client` fixture. Every test
gets a new in-memory SQLite database, so tests are fast and cannot damage the
development `tasks.db`.

The fixture replaces `get_db` through FastAPI dependency overrides:

```python
app.dependency_overrides[get_db] = override_get_db
```

This is an important benefit of dependency injection: production and tests use
the same route, service, repository, and model code; only the database changes.

## Test structure

Use Arrange, Act, Assert:

```python
def test_create_user(client: TestClient) -> None:
    # Arrange: prepare input.
    payload = {"name": "Budi", "email": "budi@example.com"}

    # Act: call the public API.
    response = client.post("/api/v1/users", json=payload)

    # Assert: verify observable behavior.
    assert response.status_code == 201
    assert response.json()["name"] == "Budi"
```

## Minimum test checklist for a CRUD resource

- Create returns `201` and the saved fields.
- List returns records in the expected order.
- Pagination works.
- Read returns the requested record.
- Patch changes only submitted fields.
- Delete returns `204`, then read returns `404`.
- Missing IDs return `404`.
- Invalid input returns `422`.
- Each important business rule has a test.

Run all tests from the project root:

```powershell
pytest -q
```

Do not make tests depend on their execution order. Each test should arrange its
own data and should pass when run alone.
