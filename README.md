# DistillERP

DistillERP is a FastAPI + PostgreSQL backend with a Vite/React frontend.

## Project Structure

```text
backend/
  main.py                 FastAPI application entry point
  app/core/               Settings, database, auth, rate limiting
  app/models/             SQLAlchemy models
  app/routers/            API routes
  app/schemas/            Pydantic schemas
  app/services/           Business services
  seed_users.py           Initial admin user seeding script
frontend/
  src/                    React app
  public/                 Static public assets
  package.json            Vite scripts and dependencies
Dockerfile                Railway production build
railway.json              Railway health check and Docker builder config
```

## Local Development

Backend:

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Frontend:

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

## Railway Deployment

This repository is prepared for a single Railway web service. The Dockerfile builds the React frontend, copies the generated `frontend/dist` bundle into the runtime image, and serves the app from FastAPI. API calls use the same origin by default, so `VITE_API_URL` is not required in production.

1. Push this repository to GitHub.
2. Create a Railway project and add a PostgreSQL database service.
3. Add a new service from the GitHub repo.
4. Railway will detect `Dockerfile` and use `railway.json`.
5. Set the app service variables:

```text
DATABASE_URL=<reference the Railway PostgreSQL DATABASE_URL>
SECRET_KEY=<generate a long random value>
ENVIRONMENT=production
ALLOWED_ORIGINS=https://your-app-domain.railway.app
BACKUP_PATH=/app/data/backups
```

6. Generate a public domain for the app service.
7. Confirm `/health` returns `{"status":"healthy","environment":"production"}`.
8. Seed initial users once from the app service shell:

```bash
python seed_users.py
```

Change the seeded default passwords immediately after the first login.

## Notes

- Do not commit `.env` files. Configure secrets in Railway variables.
- If Railway gives you a Postgres variable under a different name, the backend also accepts `DATABASE_PRIVATE_URL`, `POSTGRES_URL`, or `POSTGRES_PRIVATE_URL`.
- The backup directory is inside the container by default. Attach a Railway volume and set `BACKUP_PATH` to the mounted path if backups must survive redeploys.
- For separate frontend/backend services, set `VITE_API_URL` to the backend public URL during the frontend build and set `ALLOWED_ORIGINS` to the frontend public URL.
