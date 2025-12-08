<!-- Copilot / AI agent instructions tailored for the `db-l2-amora` project -->
# Project quick-orientation for AI coding agents

Purpose: Help an AI become productive quickly in this FastAPI + Postgres example project.

Key files (read these first):
- `app.py` — FastAPI entrypoint. Endpoints call `get_connection()` then delegate to `db.py` functions.
- `db.py` — Database query functions. Functions accept a `conn` and use `RealDictCursor`. They often `raise HTTPException` for 404s and return cursor results.
- `db_setup.py` — `get_connection()` and `create_tables()` helper (used as a lightweight migration script).
- `schemas.py` — Pydantic models used by endpoints (e.g., `UserCreate`, `PropertyFullCreate`).
- `readme.md` — project notes and suggested workflow.
- `requirements.txt` — minimal runtime deps: `psycopg2-binary`, `fastapi[standard]`.

Big-picture architecture and patterns
- Runtime: FastAPI app is `app` in `app.py`. Uvicorn is expected to run it (`uvicorn app:app --reload`).
- DB access pattern: each endpoint calls `get_connection()` (from `db_setup.py`) and passes the connection to `db.py` functions. Query functions use `with conn:` and `with conn.cursor(cursor_factory=RealDictCursor)`.
- Validation: Request bodies use Pydantic models found in `schemas.py`. Use those models when adding or updating resources.
- Response style: Endpoints return dictionaries like `{"user": user}` or raise `HTTPException` for errors.

Project-specific conventions and gotchas (use these to guide code edits)
- Use `get_connection()` at the start of endpoints instead of global/persistent connections. Be conservative: the project doesn't use connection pooling.
- DB functions should accept `conn` as the first parameter and return either a dict/rows or raise `HTTPException` when a resource is missing. Example: `get_user(conn, user_id)` returns a user or raises 404.
- SQL helpers use `RealDictCursor` and `.fetchone()` / `.fetchall()`; preserve that style for new functions.
- Pydantic models use Python 3.10 union syntax (`str | None`). Keep type style consistent with `schemas.py`.

Concrete examples from the codebase
- Endpoint -> DB flow:
  - `app.post('/user/')` calls `get_connection()` then `add_user(conn, user)` and returns the created resource.
  - `app.get('/property/{property_id}')` calls `get_property_by_id(get_connection(), property_id)` and returns `{"property": property}`.
- DB function pattern:
  - Use `with conn:` and `with conn.cursor(cursor_factory=RealDictCursor) as cursor:`
  - `cursor.execute(sql, params)` then `cursor.fetchone()` or `cursor.fetchall()`
  - If result missing, raise `HTTPException(status_code=404, detail="...")` (see `get_user` and `get_property_by_id`).

Notable inconsistencies and bugs to watch for
- Naming: `delet_agency_by_id` in `db.py` (and imported as `delet_agency_by_id` in `app.py`) — spelling differs from `delete_*` conventions.
- Wrong delete target: `delet_agency_by_id` executes `DELETE FROM properties WHERE id = %s` (likely a copy-paste bug). Verify table names before changing behavior.
- Schema names: `vedioCreate` and `imagesCreate` are misspelled/oddly-cased. When adding similar models, follow the existing names to avoid mismatches, but consider proposing normalized names in a separate PR.
- Hardcoded connection values: `db_setup.get_connection()` currently returns a hard-coded connection (`dbname="testdb", user="amr", password="682354"`). The file loads `.env` but does not use `DATABASE_NAME` / `PASSWORD`. Prefer editing `get_connection()` to read env vars before running locally.
- SQL case mismatch: some SQL uses uppercase table names (e.g., `INSERT INTO FEATURES`) — Postgres folds unquoted identifiers to lower-case; ensure cases and quoting are correct when writing queries.

Developer workflows (how to run and debug locally)
- Install deps and create a venv (bash on Windows):
  ```bash
  python -m venv .venv
  source .venv/Scripts/activate    # on Windows Git Bash / WSL use the Scripts path
  pip install -r requirements.txt
  ```
- Start DB (you must provide a running Postgres instance). Either update `db_setup.get_connection()` to use your `DATABASE_NAME`, `USER`, and `PASSWORD` from a `.env` file, or create a DB/user that matches the hard-coded values.
- Create tables (migration step):
  ```bash
  python db_setup.py
  # prints "Tables created successfully." on success
  ```
- Run the API server:
  ```bash
  uvicorn app:app --reload
  # then open http://localhost:8000/docs
  ```

Testing and verification notes
- No automated tests are present. Manual checks:
  - Use Swagger at `/docs` to exercise endpoints.
  - Create sample users/properties and validate DB rows with `psql` or a GUI.

When modifying code, be conservative and run quick manual smoke tests:
- After changing a DB query, run the endpoint that depends on it and confirm expected JSON and DB state.
- When renaming functions (e.g., fix `delet_agency_by_id` -> `delete_agency_by_id`), update `app.py` imports and endpoints at the same time to avoid runtime import errors.

If you need to extend the project
- Add new endpoints in `app.py` following the simple pattern: `conn = get_connection(); result = db_fn(conn, params); return { ... }`.
- Place new DB helpers in `db.py` and follow the `with conn:` pattern plus `RealDictCursor`.
- Add Pydantic models in `schemas.py` and use them as request body types in endpoints.

Questions for the repo owner (answering these will make future AI work safer):
- Should `get_connection()` be updated to read environment variables by default (recommended)?
- Are naming fixes (typos listed above) allowed in a single PR, or do you prefer smaller focused PRs?

If anything in this file is unclear or missing, tell me which area you want expanded (running tests, env setup, example endpoint change), and I'll iterate.

**Live suggestions (in-editor)**
- Purpose: Proactively offer short, focused suggestions while the developer edits files. Keep suggestions minimal, actionable, and safe to apply.
- When to suggest:
  - On file open for key files: `app.py`, `db.py`, `db_setup.py`, `schemas.py`.
  - After the user pauses typing (~1–2 seconds) inside a function or SQL string.
  - When the user saves the file if the editor signals a save event.
- What to suggest (examples taken from this repo):
  - Typo fixes: e.g. propose renaming `delet_agency_by_id` -> `delete_agency_by_id` and updating its callers in `app.py`.
  - Bug fixes: e.g. point out `INSERT INTO FEATURES` vs. `INSERT INTO features` (Postgres identifier case) and suggest corrected SQL.
  - Security/safety: warn about hard-coded credentials in `db_setup.get_connection()` and suggest replacing with `os.getenv()` usage and `.env` values.
  - API/DB patterns: when you see a new endpoint, suggest using `get_connection()` then a `db.py` helper that follows the `with conn:` + `RealDictCursor` pattern.
  - Parameter bugs: detect suspicious `cursor.execute(..., (values))` where `values` is a list instead of a tuple and recommend converting to a tuple and matching placeholder order.
  - Small refactors: suggest extracting repeated SQL parts into helpers when you detect duplication across functions (keep proposals minimal).
- Suggestion format and delivery:
  - Provide a one-line summary, a short rationale (1–2 lines), and a minimal code patch (diff or single-file edit). Example:
    - Summary: "Fix typo: rename `delet_agency_by_id` to `delete_agency_by_id` and update imports."
    - Rationale: "Naming inconsistency risks runtime import errors; callers in `app.py` import `delet_agency_by_id`."
    - Patch: show the exact `apply_patch`-style edit or a small suggested replacement snippet.
- Guardrails (must follow these):
  - Never change high-level behavior without asking (e.g., do not change SQL logic that alters data semantics without confirmation).
  - Keep style and patterns consistent with existing files (use `RealDictCursor`, `with conn:` blocks, and Pydantic models as shown).
  - When suggesting edits that affect multiple files, list all files to change and offer to apply the patch only after approval.
- Quick examples you can offer inline for `db.py` edits:
  - Fix delete function name and SQL target (conservative patch):
    - Rename `delet_agency_by_id` -> `delete_agency_by_id`.
    - Confirm SQL should be `DELETE FROM agencies WHERE id = %s RETURNING id` (not `properties`).
  - Fix hard-coded `get_connection()` usage (suggestion only): replace constants with `os.getenv('DATABASE_NAME', 'testdb')`, `os.getenv('USER', 'amr')`, and `os.getenv('PASSWORD')` and document required `.env` keys.

If you'd like a different suggestion cadence (e.g., silent until requested, or aggressive inline fixes), tell me your preference and I'll adapt these rules.
