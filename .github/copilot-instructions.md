# Copilot instructions for the `notebook` project

This file gives concise, actionable guidance for AI coding agents working on this repository.

Overview
- **Purpose**: Small Flask app that exposes a simple application factory and MySQL-backed persistence.
- **Key entrypoints**: `create_app()` in [notebook/__init__.py](notebook/__init__.py#L1-L40), configuration in [notebook/config.py](notebook/config.py#L1-L200), and DB helpers in [notebook/db.py](notebook/db.py#L1-L400).

Architecture & patterns (what matters)
- The app uses the Flask application factory pattern: implement or modify `create_app()` when adding extensions or blueprints (`create_app()` in [notebook/__init__.py](notebook/__init__.py#L1-L40)).
- Configuration is layered: defaults via `app.config.from_mapping()`, then an untracked instance file `instance/config.py`, then environment variables (see [notebook/config.py](notebook/config.py#L1-L200)). Prefer changing `instance/config.py` or environment variables rather than source.
- DB connection lifecycle: a single PyMySQL connection is stored on Flask's `g` as `g.db` and closed on teardown; use `get_db()` and let teardown close it automatically ([notebook/db.py](notebook/db.py#L1-L400)).
- CLI extension: `init_db` is registered as a Flask CLI command and reads `instance/schema.sql` to initialize schema; the loader naively splits SQL by semicolons — avoid complex statements that contain semicolons inside literals ([notebook/db.py](notebook/db.py#L1-L400)).

Developer workflows (concrete commands)
- Run the app (development):

  - `export FLASK_APP=notebook`
  - `export FLASK_ENV=development` (optional)
  - `flask run`

- Initialize the DB schema (after creating `instance/schema.sql` and setting DB creds):

  - Ensure `DB_USER` and `DB_PASSWORD` are set in the environment or in `instance/config.py`.
  - `flask init-db` (this executes the statements found in `instance/schema.sql`).

Project-specific conventions & gotchas
- Secrets are deliberately kept out of source. Put secrets in `instance/config.py` (which is ignored/untracked) or supply via env vars: `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`, `DB_NAME`, `SECRET_KEY` ([notebook/config.py](notebook/config.py#L1-L200)).
- `app.instance_path` is created at startup (see `makedirs` in `create_app()`); expect `instance/schema.sql` and `instance/config.py` there.
- DB creation: `get_db()` will attempt to create the database if it does not exist — this requires admin-level DB credentials or a user with CREATE DATABASE privileges. The code uses `pymysql` and `autocommit=True` with `DictCursor` ([notebook/db.py](notebook/db.py#L1-L400)).
- SQL loader is simple: it splits on `;` and executes non-empty statements. If adding migrations or complex schema scripts, prefer a migration tool or adapt the loader.

Integration points & dependencies
- Requires a running MySQL-compatible server and the `PyMySQL` package (imported as `pymysql` in [notebook/db.py](notebook/db.py#L1-L400)).
- The app exposes CLI commands via Flask's CLI; tests or automation that invoke `flask` should set `FLASK_APP=notebook`.

Examples of actionable edits
- Add an extension: modify `create_app()` in [notebook/__init__.py](notebook/__init__.py#L1-L40) to call the extension's init_app; follow the existing `init_config(app)` and `init_db(app)` pattern.
- Add a blueprint: register it within `create_app()` so the app factory remains the single place that wires components.
- Change DB defaults: update `app.config.setdefault(...)` in [notebook/db.py](notebook/db.py#L1-L400) rather than hardcoding elsewhere.

Testing & debugging notes
- To debug DB connection issues, verify `DB_USER`/`DB_PASSWORD` are set; the code raises a clear `RuntimeError` when credentials are missing ([notebook/db.py](notebook/db.py#L1-L120)).
- When modifying the schema loader, add a unit test that places a sample `schema.sql` into a temporary `instance_path` and runs the `init-db` command via Flask's test CLI.

When in doubt
- Do not add secrets to source. Prefer adding instance-level files or environment variables.
- Preserve the application-factory pattern and keep wiring inside `create_app()`.

If any of these sections are unclear or you want more examples (e.g., a sample `instance/config.py` or a safer SQL loader), tell me which area to expand.
