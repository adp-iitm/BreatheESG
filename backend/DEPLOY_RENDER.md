# Backend deployment (Render)

## Files used

- `backend/requirements.txt`
- `backend/Procfile`
- `backend/build.sh`
- `backend/runtime.txt`
- `backend/.env.example`
- `render.yaml`

## Deploy

1. Push repository to GitHub.
2. In Render, create a new Blueprint deploy from this repository.
3. Render will provision:
   - `esg-postgres` database
   - `esg-backend` web service
4. Ensure env vars are set:
   - `DJANGO_SECRET_KEY`
   - `DEBUG=0`
   - `ALLOWED_HOSTS`
   - `CORS_ALLOWED_ORIGINS`
   - `DATABASE_URL` (from Render PostgreSQL)
5. Deployment build runs:
   - `./build.sh` -> install deps, `migrate`, `collectstatic`
6. Web process starts via:
   - `gunicorn config.wsgi:application`
