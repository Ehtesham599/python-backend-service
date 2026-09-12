# Python Backend Service

A minimal, Flask template for building backend services and
APIs. Use this repo as a starting point when spinning up a new service: clone it, rename the package, and start adding routes.

## What's included

- **Flask application factory** ([app/__init__.py](app/__init__.py)) — the
  app is built by `create_app()` rather than as a module-level global, so it
  can be configured differently for tests vs. production.
- **Versioned routes as blueprints** ([app/routes/v1/health.py](app/routes/v1/health.py))
  — routes are grouped by API version under `app/routes/<version>/` and
  registered as Flask blueprints in `create_app()`.
- **Request validation with Pydantic** ([app/schemas/hello.py](app/schemas/hello.py))
  — query/body payloads are parsed into Pydantic models; validation errors
  are turned into `400` responses automatically.
- **Centralized error handling** — 404s, Pydantic `ValidationError`s, other
  HTTP exceptions, and any unhandled exception all get consistent JSON error
  responses instead of leaking stack traces or default Flask error pages.
- **Structured JSON logging** ([app/logging_config.py](app/logging_config.py))
  — logs are emitted as single-line JSON to stdout, ready to ship to a log
  aggregator.
- **Tests with pytest** ([tests/](tests/)) — a `client` fixture builds the
  app via `create_app()` and exercises it through Flask's test client.

## Project structure

```
.
├── app/
│   ├── __init__.py            # application factory: create_app()
│   ├── logging_config.py      # JSON logging setup
│   ├── routes/
│   │   └── v1/
│   │       └── health.py      # example blueprint for API v1
│   └── schemas/
│       └── hello.py           # Pydantic request models
├── tests/
│   ├── conftest.py            # test path setup
│   ├── test_sanity.py
│   └── v1/
│       └── test_health_routes.py
├── main.py                    # dev entrypoint (app.run)
├── requirements.txt
├── .env.example                # documents expected environment variables
└── .python-version
```

## Requirements

- Python 3.11 (see [.python-version](.python-version))

## Getting started

1. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Copy the environment file and fill in any values your service needs:

   ```bash
   cp .env.example .env
   ```

4. Run the service:

   ```bash
   python main.py
   ```

   The app starts on `http://0.0.0.0:8000` with the reloader/debugger
   enabled (`debug=True` in [main.py](main.py) — turn this off before
   deploying).

5. Try the example endpoints:

   ```bash
   curl http://localhost:8000/hello_world
   curl "http://localhost:8000/hello?name=Alice"
   ```

A VS Code launch configuration for `main.py` is already set up in
[.vscode/launch.json](.vscode/launch.json) (Run and Debug → "Python: Run main.py").

## Running tests

```bash
pytest
```

Tests use Flask's test client via the `client` fixture in
[tests/conftest.py](tests/conftest.py) and [tests/v1/test_health_routes.py](tests/v1/test_health_routes.py),
so no running server is required.

## Using this as a template

### Add a new endpoint

1. Add a Pydantic model for the request payload (if any) under
   `app/schemas/`, e.g. `app/schemas/widget.py`.
2. Create or extend a blueprint under `app/routes/<version>/`, e.g.
   `app/routes/v1/widgets.py`:

   ```python
   from flask import Blueprint, jsonify, request
   from app.schemas.widget import CreateWidgetModel

   widgets_bp = Blueprint('widgets', __name__)

   @widgets_bp.route('/widgets', methods=['POST'])
   def create_widget():
       payload = CreateWidgetModel.model_validate(request.get_json(force=True))
       # ... business logic ...
       return jsonify({"id": "..."}), 201
   ```

3. Register the blueprint in `create_app()` in [app/__init__.py](app/__init__.py):

   ```python
   from app.routes.v1.widgets import widgets_bp
   app.register_blueprint(widgets_bp)
   ```

4. Add tests under `tests/v1/` following the pattern in
   [tests/v1/test_health_routes.py](tests/v1/test_health_routes.py).

### Add a new API version

Create a new package `app/routes/v2/`, add blueprints there, and register
them alongside (or instead of) the v1 blueprints in `create_app()`. Keeping
routes namespaced by version makes it straightforward to run v1 and v2
side by side during a migration.

### Error handling

Don't add per-route try/except blocks for generic failures — the
application-level handlers in [app/__init__.py](app/__init__.py) already
cover:

- `404` — unknown routes
- Pydantic `ValidationError` — invalid request payloads → `400`
- `HTTPException` — any `abort(...)` or Werkzeug HTTP error, logged and
  returned with its original status code
- any other `Exception` — logged and returned as a generic `500`

Only add a route-specific handler when an endpoint needs a different status
code or response shape than these defaults.

### Logging

Use the standard `logging` module; the root logger is already configured
by `setup_logging()` to emit structured JSON to stdout:

```python
import logging
logging.info("something happened", extra={"extra_payload": {"widget_id": widget_id}})
```

### Configuration

Environment variables are documented in [.env.example](.env.example) —
copy it to `.env` for local development (loaded via `python-dotenv` /
`os.environ` as needed). Add new variables there as you introduce them so
the file stays the source of truth for required configuration.

## Dependencies

See [requirements.txt](requirements.txt):

- `flask` — web framework
- `pydantic` — request/response validation
- `requests` / `httpx` — HTTP clients for calling other services
- `python-dotenv` — loads `.env` for local development
- `pytest` — test runner
