# SR 11-7 Gap Scanner

**Free SR 11-7 Model Risk Management Self-Assessment for Mid-Market Lenders**

A public-facing web application that scores a financial institution's SR 11-7 compliance posture across all 12 control domains. Produces a gap heatmap PDF report and captures discovery call leads for ILOL.

🔗 **Live:** [scanner.ilol.ai](https://scanner.ilol.ai) · **API Docs:** [API on Cloud Run](https://sr117-scanner-api.a.run.app/docs)

---

## What It Does

1. User fills a 36-question, 12-domain SR 11-7 self-assessment (5 min)
2. Backend scores each domain (RED/AMBER/GREEN), computes a weighted overall score (0–100)
3. A styled PDF report is auto-generated and emailed — no gate
4. Personalized remediation guidance is offered via a free 20-min discovery call booking (Calendly CTA)

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Next.js 14 App Router (TypeScript) · Tailwind CSS · Recharts |
| Backend | FastAPI (Python 3.11) · ReportLab (PDF) |
| Lead Store | Supabase (Postgres) or local JSON fallback |
| Email | Resend (primary) · SendGrid (fallback) |
| PDF Storage | GCP Cloud Storage |
| Deployment | Vercel (frontend) · GCP Cloud Run (backend) |
| CI/CD | GitHub Actions |

---

## Local Setup

### Prerequisites
- Docker & Docker Compose
- Node.js 20+ (for frontend-only dev)
- Python 3.11+ (for backend-only dev)

### 1. Clone and configure

```bash
git clone https://github.com/YOUR_ORG/sr117-gap-scanner.git
cd sr117-gap-scanner
cp .env.example .env
# Edit .env with your API keys (email provider is optional for local dev)
```

### 2. Run with Docker Compose

```bash
docker-compose up --build
```

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API docs: http://localhost:8000/docs

### 3. Run without Docker (dev mode)

**Backend:**
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

---

## Environment Variables

### Backend (`.env` or Cloud Run secrets)

| Variable | Required | Description |
|---|---|---|
| `RESEND_API_KEY` | Optional* | Resend API key for email delivery |
| `SENDGRID_API_KEY` | Optional* | SendGrid fallback for email |
| `FROM_EMAIL` | No | Sender address (default: `reports@ilol.ai`) |
| `GCP_PROJECT_ID` | Optional | GCP project for Cloud Storage |
| `GCP_BUCKET_NAME` | No | GCS bucket (default: `sr117-reports`) |
| `SUPABASE_URL` | Optional | Supabase project URL for lead storage |
| `SUPABASE_KEY` | Optional | Supabase anon key |
| `CALENDLY_LINK` | No | Calendly booking link in PDF CTA |
| `ALLOWED_ORIGINS` | No | CORS origins (comma-separated) |

*If no email provider is configured, emails are skipped and a warning is logged. Leads are stored locally to `backend/data/leads.json`.

### Frontend (`.env.local` or Vercel settings)

| Variable | Required | Description |
|---|---|---|
| `NEXT_PUBLIC_BACKEND_URL` | Yes | Backend API base URL |
| `NEXT_PUBLIC_CALENDLY_LINK` | No | Calendly link for CTA widget |

---

## Project Structure

```
sr117-gap-scanner/
├── frontend/                    # Next.js 14 App Router
│   ├── app/
│   │   ├── page.tsx             # Landing page
│   │   ├── scanner/page.tsx     # Multi-step form
│   │   ├── scanner/results/     # Results + heatmap + CTA
│   │   └── api/submit/          # API route → backend
│   ├── components/
│   │   ├── AssessmentForm.tsx   # 13-step assessment wizard
│   │   ├── DomainCard.tsx       # Per-domain question card
│   │   ├── GapHeatmap.tsx       # 12-row RAG heatmap table
│   │   ├── ScoreGauge.tsx       # Radial score gauge
│   │   └── CTABookCall.tsx      # Calendly CTA block
│   └── lib/
│       ├── domains.ts           # 12 SR 11-7 domain definitions
│       └── scoring.ts           # Client-side scoring
├── backend/
│   ├── main.py                  # FastAPI app
│   ├── routers/
│   │   ├── assessment.py        # POST /api/v1/assess
│   │   └── report.py            # POST /api/v1/report (async)
│   ├── services/
│   │   ├── scorer.py            # Domain scoring engine
│   │   ├── pdf_generator.py     # ReportLab PDF generator
│   │   ├── lead_store.py        # Supabase / local lead storage
│   │   └── email_sender.py      # Resend / SendGrid email
│   └── tests/
│       └── test_scorer.py       # Pytest scoring tests
├── .github/workflows/
│   ├── ci.yml                   # Lint + test on PR
│   └── deploy.yml               # Deploy on push to main
├── deploy/
│   ├── cloudbuild.yaml          # GCP Cloud Build pipeline
│   └── vercel.json              # Vercel deployment config
├── docker-compose.yml
├── Dockerfile.backend
└── Dockerfile.frontend
```

---

## The 12 SR 11-7 Domains

| # | Domain | Weight | SR 11-7 Section |
|---|---|---|---|
| 1 | Model Inventory & Classification | 1.0x | §4.1 |
| 2 | Model Development Documentation | 1.0x | §4.2 |
| 3 | **Model Validation Independence** | **1.3x** | §4.3 |
| 4 | Conceptual Soundness Review | 1.0x | §4.3.1 |
| 5 | **Ongoing Monitoring & Performance** | **1.3x** | §4.4 |
| 6 | Model Change Management | 1.0x | §4.4.1 |
| 7 | Outcomes Analysis & Back-testing | 1.0x | §4.4.2 |
| 8 | Model Use Policy & Governance | 1.0x | §5.1 |
| 9 | Third-Party / Vendor Model Oversight | 1.0x | §5.2 |
| 10 | Data Quality & Data Governance | 1.0x | §5.3 |
| 11 | **Fair Lending / Disparate Impact** | **1.3x** | §5.4 |
| 12 | Board & Senior Management Oversight | 1.0x | §6.0 |

Domains 3, 5, 11 are weighted 1.3x — highest examiner enforcement frequency in 2025–2026.

---

## Scoring

```
domain_pct = (raw_score / max_raw) × 100
  RED   < 40%
  AMBER 40–69%
  GREEN ≥ 70%

weighted_sum = Σ (domain_raw / domain_max × 3.0 × domain_weight)
max_weighted  = Σ (3.0 × domain_weight)
overall_score = (weighted_sum / max_weighted) × 100
  RED   < 50
  AMBER 50–74
  GREEN ≥ 75
```

---

## Deployment

### Backend → GCP Cloud Run

```bash
gcloud builds submit --config deploy/cloudbuild.yaml \
  --project YOUR_PROJECT_ID \
  --substitutions=COMMIT_SHA=$(git rev-parse HEAD)
```

Set secrets in Cloud Run:
- `RESEND_API_KEY`, `SUPABASE_URL`, `SUPABASE_KEY` via Secret Manager

### Frontend → Vercel

```bash
cd frontend
vercel --prod
```

Set environment variables in Vercel dashboard:
- `NEXT_PUBLIC_BACKEND_URL` → your Cloud Run URL

### GitHub Actions Secrets Required

| Secret | Description |
|---|---|
| `GCP_WORKLOAD_IDENTITY_PROVIDER` | Workload Identity Federation provider |
| `GCP_SERVICE_ACCOUNT` | GCP service account email |
| `GCP_PROJECT_ID` | GCP project ID |
| `VERCEL_TOKEN` | Vercel deploy token |
| `NEXT_PUBLIC_BACKEND_URL` | Cloud Run backend URL |
| `NEXT_PUBLIC_CALENDLY_LINK` | Calendly booking URL |

---

## Running Tests

```bash
cd backend
pip install pytest pytest-asyncio httpx
pytest tests/ -v
```

---

## Definition of Done

- [x] `docker-compose up` → app at `localhost:3000` ✓
- [x] 12 fully scored domains ✓
- [x] Weighted scoring engine (1.3x for domains 3, 5, 11) ✓
- [x] PDF report with cover, heatmap, RED domain detail, enforcement citations, CTA ✓
- [x] Email delivery via Resend / SendGrid ✓
- [x] Lead storage to Supabase / local fallback ✓
- [x] GCP Cloud Storage for PDF files ✓
- [x] GitHub Actions CI (lint + test) ✓
- [x] GitHub Actions deploy (Cloud Run + Vercel) ✓
- [x] Mobile-responsive Tailwind UI ✓
- [x] Ungated PDF, gated remediation roadmap ✓

---

## Built By

**ILOL — Integrated Lending Operations Lab**  
ilol.ai · contact@ilol.ai

> Compliance infrastructure for mid-market lenders.
