# HSATracker
HSATracker is a free, self-hosted HSA receipt and reimbursement tracker built for privacy-conscious users who want full control over their sensitive medical financial data. No subscriptions, no third-party servers, no data mining.

# HSATracker — Build Progress

## Overview

HSATracker is a self-hosted, privacy-first alternative to Shoebox.io and TrackHSA.com.
All data stays on your machine. No external services, no subscriptions.

**Stack:** React + TypeScript + Vite · FastAPI · PostgreSQL · Docker Compose

---

## Completed: Backend API (Steps 1–6)

### Step 1 — Repo Scaffolding
- `.gitignore` — ignores `__pycache__`, `node_modules`, `.env`, `data/`
- `docker-compose.yml` — three services: `db`, `backend`, `frontend`
- `.env.example` — all required environment variables with safe defaults

### Step 2 — Database Schema & Migrations
Alembic migration `0001_initial` creates all 5 tables:

| Table | Purpose |
|---|---|
| `expenses` | Medical expense records |
| `reimbursements` | HSA reimbursement tracking per expense |
| `contributions` | HSA contribution records by tax year |
| `account_balance` | Point-in-time HSA balance snapshots |
| `receipts` | File attachment metadata per expense |

All money columns use `NUMERIC(10,2)`. UUIDs for all primary keys.
Alembic runs automatically on container startup (`alembic upgrade head`).

### Step 3 — Expenses API
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/v1/expenses/` | List with filters: `year`, `category`, `payment_method` |
| `POST` | `/api/v1/expenses/` | Create expense |
| `GET` | `/api/v1/expenses/{id}` | Detail with nested reimbursement + receipts |
| `PATCH` | `/api/v1/expenses/{id}` | Partial update |
| `DELETE` | `/api/v1/expenses/{id}` | Delete (cascades to reimbursement + receipts) |

### Step 4 — Reimbursements API
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/v1/reimbursements/` | List with `status` filter; includes `pending_amount` and `reimbursed_amount_ytd` totals |
| `POST` | `/api/v1/reimbursements/` | Mark expense as pending reimbursement |
| `PATCH` | `/api/v1/reimbursements/{id}` | Update status, date, amount |
| `DELETE` | `/api/v1/reimbursements/{id}` | Remove reimbursement record |

**Business logic enforced:**
- Only `out_of_pocket` expenses can be reimbursed (400 if HSA-paid)
- Duplicate reimbursement records are rejected (400)

### Step 5 — Contributions, Balance & Summary APIs
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/v1/contributions/` | List by `tax_year`; includes IRS limits and remaining amounts |
| `POST` | `/api/v1/contributions/` | Record a contribution |
| `PATCH` | `/api/v1/contributions/{id}` | Update contribution |
| `DELETE` | `/api/v1/contributions/{id}` | Delete contribution |
| `GET` | `/api/v1/balance/` | All balance snapshots + `latest` |
| `POST` | `/api/v1/balance/` | Add balance snapshot |
| `DELETE` | `/api/v1/balance/{id}` | Remove snapshot |
| `GET` | `/api/v1/summary/` | Dashboard aggregate: expenses, reimbursements, contributions, balance |

**IRS contribution limits (built-in):**
- 2024: $4,150 individual / $8,300 family
- 2025–2026: $4,300 individual / $8,550 family

### Step 6 — Receipt File Upload
| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/v1/expenses/{id}/receipts/` | Upload file (JPG, PNG, PDF) |
| `GET` | `/api/v1/expenses/{id}/receipts/` | List receipt metadata for expense |
| `GET` | `/api/v1/receipts/{id}/file` | Stream file inline (renders in browser) |
| `DELETE` | `/api/v1/receipts/{id}` | Delete record + file from disk |

**Storage:** Files saved to `./data/uploads/` on the host via Docker bind mount.
Renamed to `{uuid}.ext` on disk to prevent collisions. Max size configurable via `MAX_UPLOAD_SIZE_MB` (default 10MB).

---

## Docker Compose Services

```
db        postgres:17-alpine     Named volume: postgres_data
backend   python:3.13-slim       Bind mount: ./data/uploads → /app/uploads
frontend  (not yet built)        Host port: ${PORT:-3000}
```

Start the backend stack:
```bash
cp .env.example .env        # set a real POSTGRES_PASSWORD
docker compose up db backend --build -d
docker compose logs backend  # confirm "Application startup complete"
```

---

## Remaining Steps

| Step | Description |
|---|---|
| 7 | Frontend scaffold — Vite, React, Tailwind, React Router |
| 8 | Frontend: shared infra — API client, TypeScript types, Layout |
| 9 | Frontend: expenses page + form modal |
| 10 | Frontend: receipts — upload, list, thumbnail |
| 11 | Frontend: reimbursements page |
| 12 | Frontend: contributions + IRS limit bar |
| 13 | Frontend: dashboard + balance page |
| 14 | Docker production build — frontend Dockerfile + Nginx |
| 15 | Polish — toasts, empty states, loading skeletons, README |

