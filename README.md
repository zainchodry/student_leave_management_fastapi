**Student Leave Management (FastAPI)**

- **Project**: Student Leave Management is a lightweight REST API built with FastAPI to manage users, profiles, departments, attendance, leave requests, notifications, and password resets for an educational institution or organization.

**Features**

- **API**: CRUD endpoints for users, profiles, departments, attendance, leave requests, and notifications.
- **Auth**: Token-based authentication and role helpers.
- **Email**: Utilities for OTP and password reset emails.
- **Database**: SQLAlchemy models with a centralized `database.py` connection.
- **Docs**: Auto-generated OpenAPI docs at `/docs` and `/redoc` when running the app.

**Tech Stack**

- **Framework**: FastAPI
- **ORM**: SQLAlchemy (project models in `app/models`)
- **Server**: Uvicorn
- **Python**: 3.10+ recommended

**Prerequisites**

- Python 3.10 or newer
- pip (or pipx/virtualenv)

**Quickstart (development)**

1. Create and activate a virtual environment (recommended):

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Configure environment variables: create a `.env` file in the project root with at least the following values (example):

```env
DATABASE_URL=sqlite:///./dev.db
SECRET_KEY=your-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=60
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USER=you@example.com
SMTP_PASS=secret
```

4. Run the app (development):

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

5. Open the API docs: http://127.0.0.1:8000/docs

**Project Layout**

- **app/**: application package
  - **models/**: SQLAlchemy model definitions (`user.py`, `leave.py`, `attendance.py`, etc.)
  - **routes/**: API route modules
  - **schemas/**: Pydantic request/response schemas
  - **utils/**: helpers for auth, email, otp, roles, security
  - `main.py`: FastAPI app factory / startup
  - `database.py`: DB connection and session utilities

**Database & Migrations**

- The project uses SQLAlchemy models. For schema migrations, consider adding Alembic. Example minimal commands (after installing alembic and configuring `alembic.ini`):

```bash
alembic revision --autogenerate -m "init"
alembic upgrade head
```

If you're using SQLite for development, the `DATABASE_URL` example above will create `dev.db` in the project root.

**Testing**

- Add tests under a `tests/` directory and run with `pytest`:

```bash
pytest
```

**Environment files & security**

- Do not commit `.env` or secrets. The repository already includes a `.gitignore` that ignores `.env`, virtualenvs, and sensitive artifacts.

**Running in Production**

- Use a production ASGI server (e.g., `gunicorn -k uvicorn.workers.UvicornWorker`) behind a reverse proxy.
- Use a robust RDBMS (Postgres recommended) and configure `DATABASE_URL` accordingly.

**Contributing**

- Fork the repo, create feature branches, run tests, and submit PRs.

**Reference Files**

- Application entry: [app/main.py](app/main.py)
- Database configuration: [app/database.py](app/database.py)
- Models: [app/models](app/models)

**License**

- This repository does not include a license file. Add one (for example, MIT) if you intend to open-source the project.

---

If you'd like, I can:

- add a `requirements.txt` from the environment,
- scaffold `alembic` migrations, or
- add a short Postgres production example and `docker-compose`.
