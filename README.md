# ESG Emissions Ingestion and Audit MVP

Minimal Django REST + React prototype for ingesting ESG activity data, preserving raw records, normalizing activity rows, and enabling analyst review with audit logs.

## Project Structure

- `backend/` Django + DRF API
  - `apps/ingestion/` upload + raw storage + datasource tracking
  - `apps/normalization/` mapping + validation + normalized activity
  - `apps/review/` approve/reject workflow
  - `apps/audit/` immutable audit log entries
- `frontend/` React + Tailwind analyst UI
- `docs/` architecture and design notes

## Backend Setup

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python manage.py makemigrations
python manage.py migrate
python manage.py shell -c "from apps.ingestion.models import Company; Company.objects.get_or_create(id=1, defaults={'name':'Northwind Manufacturing','industry':'Industrial'})"
python manage.py seed_demo
python manage.py runserver
```

API endpoints:

- `POST /api/upload/`
- `GET /api/datasources/`
- `GET /api/activities/` with optional `source_type`, `scope`, `review_status`
- `POST /api/activities/<id>/approve/`
- `POST /api/activities/<id>/reject/`
- `GET /api/dashboard/`

## Frontend Setup

```bash
cd frontend
npm install
copy .env.example .env
npm run dev
```

## Sample Data

Use files under `backend/sample_data/`:

- `sap_fuel.csv`
- `utility_electricity.csv`
- `travel_concur.csv`

## Deployment

### Render (Backend)

- Uses root `render.yaml`
- Set environment variables from `backend/.env.example`
- Add PostgreSQL database in Render and point `DB_*` values

### Vercel (Frontend)

- Root directory: `frontend`
- Build command: `npm run build`
- Output directory: `dist`
- Env var: `VITE_API_BASE_URL=https://<render-backend>/api`
