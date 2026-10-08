# Core: Application Configuration

[`config.py`](config.py) defines settings that may change between environments
without changing application code.

## Defaults and environment variables

```python
class Settings(BaseSettings):
    app_name: str = "Task CRUD API"
    database_url: str = "sqlite:///./tasks.db"
```

The `APP_` prefix means `database_url` can be overridden with:

```dotenv
APP_DATABASE_URL="sqlite:///./another.db"
```

See the root `.env.example` for all available values. Copy it to `.env` for
local overrides; `.env` is ignored by Git.

## Why configuration is centralized

- Development, testing, and production can use different values.
- Settings remain typed and validated.
- Other modules do not repeatedly read environment variables.
- Secrets can be injected instead of committed to source control.

Never place passwords, API keys, or real production secrets in `.env.example`.

Next: read [`../../tests/README.md`](../../tests/README.md).
