# Healthcare App — Project Documentation

> Django + DRF backend with a React frontend served as static files from Django. PostgreSQL database and JWT authentication (simplejwt) are used.

---

## Table of contents

1. Project overview
2. Quick start (local)
3. Docker (build & run)
4. Environment variables
5. Database models (summary)
6. API endpoints (routes + examples)
7. Authentication & permissions
8. Frontend integration
9. Running tests & manual API checks
10. Project structure (files & folders)
11. Development notes & best practices
12. Contributing & contact

---

## 1. Project overview

This repository implements the backend for a simple healthcare management system. Key features:

* User registration & JWT login
* CRUD APIs for Patients and Doctors
* Patient ⇄ Doctor mapping (assign / unassign)
* React frontend built and served as static files by Django home route
* PostgreSQL for production; local dev may use SQLite if configured

## 2. Quick start (local development)

**Prerequisites**

* Python 3.10+ (use pyenv or system Python)
* PostgreSQL (or use SQLite for quick local runs)
* Node.js & npm/yarn (if you plan to rebuild the React frontend)
* Git

**Steps**

1. Clone the repo

```bash
git clone https://github.com/febincf-mle/healthcare-app.git
cd healthcare-app
```

2. Create a virtual environment and activate it

```bash
python -m venv .venv
source .venv/bin/activate   # macOS / Linux
.venv\Scripts\activate     # Windows (PowerShell)
```

3. Install Python dependencies

```bash
pip install -r requirements.txt
```

4. Create a `.env` file (see Environment variables section below) and configure your database credentials.

5. Run migrations and create a superuser

```bash
python manage.py collectstatic --noinput
python manage.py migrate
python manage.py createsuperuser
```

6. Start the dev server

```bash
python manage.py runserver
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) — the React frontend is served at the Django home page; API root is under `/api/`.

## 3. Docker (build & run)

A Dockerfile is included. Quick commands from the repo root:

```bash
# build image
docker build -t health-care-app-image .

# run container (exposes port 8000)
docker run -d --name health-care-app-container -p 8000:8000 health-care-app-image
```

Adjust environment variables either via `docker run -e KEY=VALUE` flags or a docker-compose file (recommended in real deployments).

## 4. Environment variables

SET the following env variable for django settings module:
```bash
export DJANGO_SETTINGS_MODULE=config.settings.base
```

Create a `.env` (or export env vars) with at minimum the following values:

* `SECRET_KEY` — Django secret
* `POSTGRES_DB` — database name
* `POSTGRES_USER` — database user
* `POSTGRES_PASSWORD` — database password
* `POSTGRES_HOST` — host (e.g., `localhost`)
* `POSTGRES_PORT` — port (usually `5432`)
* `DJANGO_DEBUG` — `True` or `False`
* `ALLOWED_HOSTS` — comma-separated hostnames (production)
* `SIMPLE_JWT_*` — (optional) overrides for JWT lifetime/config

> Note: The project expects environment-driven settings. Keep `.env` out of version control.

## 5. Database models (summary)

(High-level; check `src` app models for exact fields.)

* **User** (custom or default `User`) — name, email, password
* **Patient** — fields such as name, age, gender, contact, created\_by (FK to User)
* **Doctor** — name, specialization, contact
* **Mapping** — relationship table linking Patients to Doctors (patient\_id, doctor\_id, created\_at)

## 6. API endpoints (routes + examples)

All APIs are prefixed with `/api/`.

### Authentication

* `POST /api/auth/register/` — Register

  * body: `{ "name": "Alice", "email": "a@example.com", "password": "pass123" }`
* `POST /api/auth/login/` — Login (returns JWT access & refresh)

  * body: `{ "email": "a@example.com", "password": "pass123" }`

**Example (curl)**

```bash
curl -X POST http://localhost:8000/api/auth/register/ \
 -H "Content-Type: application/json" \
 -d '{"name":"Alice","email":"a@example.com","password":"pass123"}'
```

### Patients (authenticated)

* `POST /api/patients/` — Create a patient
* `GET /api/patients/` — List patients created by the authenticated user
* `GET /api/patients/<id>/` — Retrieve patient details
* `PUT /api/patients/<id>/` — Update a patient
* `DELETE /api/patients/<id>/` — Delete a patient

**Example (create patient)**

```bash
curl -X POST http://localhost:8000/api/patients/ \
 -H "Authorization: Bearer <ACCESS_TOKEN>" \
 -H "Content-Type: application/json" \
 -d '{"name":"Bob","age":45,"gender":"M","contact":"9876543210"}'
```

### Doctors

* `POST /api/doctors/` — Create (Authenticated)
* `GET /api/doctors/` — List all doctors
* `GET /api/doctors/<id>/` — Retrieve doctor details
* `PUT /api/doctors/<id>/` — Update doctor
* `DELETE /api/doctors/<id>/` — Delete doctor

### Mappings (Patient ↔ Doctor)

* `POST /api/mappings/` — Assign a doctor to a patient (body: `{ "patient": <id>, "doctor": <id> }`)
* `GET /api/mappings/` — List all mappings
* `GET /api/mappings/<patient_id>/` — List doctors assigned to a patient
* `DELETE /api/mappings/<id>/` — Remove mapping

## 7. Authentication & permissions

* JWT via `djangorestframework-simplejwt` is used for token issuance and verification.
* Only authenticated users may create patients and assign doctors.
* Patients are scoped to the user who created them (i.e., list returns only those created by the requesting user).

## 8. Frontend integration

* The React app is built into static files and served by Django (home route serves the built `index.html`).
* The React app calls API endpoints under `/api/` (same-origin).


## 9. Running tests & manual API checks

* There are no automated tests included by default (add `pytest` / Django tests where suitable).
* Use Postman or `curl` to exercise endpoints. Typical workflow:

  1. `POST /api/auth/register/` → register user
  2. `POST /api/auth/login/` → get access token
  3. Use token to create patients, doctors, mappings

## 10. Project structure (high-level)

```
healthcare-app/
├─ src/                     # Django project / apps
├─ frontend/                # React app (built files may be present in repo)
├─ Dockerfile
├─ requirements.txt
├─ README.md
```

> See `src` for Django settings, app definitions, urls, and code. The repository's `requirements.txt` lists Python dependencies.

## 11. Development notes & best practices

* Use environment variables for secrets and DB credentials.
* Lock dependencies with a `requirements.txt` for reproducible builds.
* Add unit tests for serializers, views, and permissions.
* Add pagination for list endpoints if dataset grows.
* Add input validation in serializers for stricter error handling.

## 12. Contributing & contact

* To contribute: fork → feature branch → open PR. Add tests and update docs.
* For questions, open an issue on the repository or contact the maintainer listed in the repo.

---