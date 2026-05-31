# Insurance Copilot

Evidence-Based Insurance Intelligence Platform

## Architecture

```
┌─────────────────────┐      ┌──────────────────────┐
│   React 19 Frontend │─────▶│   FastAPI Backend     │
│   Vite + Tailwind   │      │   10 AI Agents        │
│   Clerk Auth        │      │   RAG Pipeline        │
└─────────────────────┘      └──────────┬───────────┘
                                        │
                            ┌───────────┴───────────┐
                            ▼                       ▼
                    ┌──────────────┐        ┌──────────────┐
                    │  PostgreSQL  │        │   Groq API   │
                    │   + pgvector │        │  llama-3.1   │
                    └──────────────┘        └──────────────┘
```

## How It Works

### 1. User Authentication
- Clerk handles sign-in/sign-up
- JWT tokens verified on every API request
- Users auto-created in PostgreSQL on first request

### 2. Policy Upload Flow
```
User uploads PDF → pdfplumber extracts text → Text stored in DB
                → Chunks created (512 tokens each)
                → Embeddings generated (all-MiniLM-L6-v2, 384-dim)
                → Stored in pgvector for similarity search
```

### 3. Policy Analysis
```
Full policy text → Groq API (128K context) → Structured JSON
               → Benefits, exclusions, waiting periods extracted
               → Stored in benefits table
               → HTML report generated
```

### 4. RAG Chat
```
User question → Query embedded → pgvector cosine search → Top 5 chunks retrieved
            → Context + question → Groq API → Answer grounded in document only
```

### 5. Claims Assessment
```
Policy data + claim details → Groq API → Eligibility score, payout estimate
                           → Coverage limits, documentation required
```

### 6. Mis-selling Detection
```
Full policy text → Groq API → Findings with evidence
               → Severity levels, red flags, user actions
```

### 7. Company Intelligence
```
Company name → Tavily web search → Groq API → Trust score, metrics
            → Claim settlement ratio, solvency ratio
```

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Frontend | React 19, TypeScript, Vite, Tailwind CSS |
| Backend | Python 3.11, FastAPI, SQLAlchemy (async) |
| Database | PostgreSQL 16 + pgvector |
| LLM | Groq API (llama-3.1-70b-versatile, 128K context) |
| Embeddings | sentence-transformers (all-MiniLM-L6-v2, local) |
| Auth | Clerk |
| Search | Tavily API |
| OCR | pdfplumber (PDF), pytesseract (images) |

## Prerequisites

- Python 3.11+
- Node.js 20+
- PostgreSQL 16+ with pgvector extension
- Groq API key (for LLM)
- Clerk account (for authentication)

## Environment Variables

### Backend (.env)

| Variable | Description | Default |
|----------|-------------|---------|
| DATABASE_URL | PostgreSQL async URL | postgresql+asyncpg://... |
| DATABASE_URL_SYNC | PostgreSQL sync URL (migrations) | postgresql+psycopg2://... |
| CLERK_API_KEY | Clerk secret key | - |
| CLERK_JWT_PUB_KEY | Clerk JWKS URL | - |
| GROQ_API_KEY | Groq API key | - |
| GROQ_MODEL | Groq model name | llama-3.1-70b-versatile |
| TAVILY_API_KEY | Tavily search API key | - |
| UPLOAD_DIR | File upload directory | uploads |
| CORS_ORIGINS | Allowed frontend origins | ["http://localhost:5173"] |

### Frontend (.env)

| Variable | Description |
|----------|-------------|
| VITE_CLERK_PUBLISHABLE_KEY | Clerk publishable key |
| VITE_API_URL | Backend API URL |

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | /health | Health check |
| GET/PUT | /api/auth/me | Current user profile |
| GET | /api/auth/stats | User statistics |
| POST | /api/policies/upload | Upload policy document |
| GET | /api/policies/ | List policies |
| GET | /api/policies/{id} | Get policy details |
| POST | /api/policies/{id}/analyze | Analyze policy with AI |
| POST | /api/chat/policy/{id} | Chat with policy (RAG) |
| POST | /api/claims/assess | Assess claim eligibility |
| POST | /api/companies/search | Research insurance company |
| POST | /api/companies/compare | Compare companies |
| POST | /api/education/explain | Explain insurance topic |
| POST | /api/education/mis-selling-check | Detect mis-selling |

## AI Agents

| Agent | Purpose |
|-------|---------|
| Policy Analysis Agent | Extracts structured policy details |
| Recommendation Agent | Generates personalized recommendations |
| Mis-selling Detection Agent | Detects misleading statements |
| Claims Assessment Agent | Analyzes claim readiness |
| Insurance Education Agent | Explains concepts simply |
| Evidence Validation Agent | Verifies factual claims |
| Grounding Validation Agent | Ensures citation accuracy |
| Report Generation Agent | Produces HTML reports |
| Company Intelligence Agent | Researches insurers |
| Research Agent | External research via Tavily |

## AI Safety Rules

1. **Never hallucinate** - Only extract information explicitly in the document
2. **Every fact** must be evidence-backed from uploaded documents
3. **Confidence system**: 🟢 Verified, 🟡 Needs Review, 🔴 Not Found
4. **Full context** - Complete policy text sent to LLM (no truncation)
5. **Simple language** - 8th-grade reading level for all user-facing content

## Database Schema

| Table | Purpose |
|-------|---------|
| users | Clerk-synced user profiles |
| policies | Uploaded policies + extracted text |
| policy_chunks | Text chunks + 384-dim embeddings |
| benefits | Structured policy benefits |
| claim_assessments | Claim evaluation results |
| mis_selling_reports | Mis-selling findings |
| recommendations | Personalized suggestions |
| companies | Insurance company data |
| audit_logs | Action audit trail |

## Quick Start

### Docker

```bash
cp BACKEND/.env.example BACKEND/.env
# Edit BACKEND/.env with your API keys

docker compose up -d postgres
docker compose up -d backend

cd FRONTEND
cp .env.example .env
npm install
npm run dev
```

### Manual Setup

```bash
# Backend
cd BACKEND
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your configuration
alembic upgrade head
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Frontend (separate terminal)
cd FRONTEND
npm install
cp .env.example .env
npm run dev
```

## Deployment

### Render (Recommended)

1. Push code to GitHub
2. Go to [render.com](https://render.com) → "New" → "Blueprint"
3. Connect your GitHub repo
4. Render detects `render.yaml` and provisions:
   - Web service (Docker)
   - PostgreSQL database with pgvector
5. Set secrets in Render dashboard:
   - `CLERK_API_KEY`
   - `CLERK_JWT_PUB_KEY`
   - `GROQ_API_KEY`
   - `TAVILY_API_KEY` (optional)
6. Deploy at `https://your-app.onrender.com`

### Docker (Self-hosted)

```bash
docker build -t insurance-copilot .
docker run -p 8000:8000 \
  -e DATABASE_URL="your_database_url" \
  -e CLERK_API_KEY="your_clerk_key" \
  -e GROQ_API_KEY="your_groq_key" \
  insurance-copilot
```

## Project Structure

```
AI_INSURANCE_COPILOT/
├── BACKEND/
│   ├── app/
│   │   ├── agents/          # 10 AI agents
│   │   ├── middleware/       # Auth, rate limiting, security
│   │   ├── models/          # SQLAlchemy ORM models
│   │   ├── routers/         # API route handlers
│   │   ├── schemas/         # Pydantic request/response
│   │   ├── services/        # Business logic (LLM, RAG, OCR, storage)
│   │   ├── config.py        # Settings
│   │   ├── database.py      # DB connection
│   │   └── main.py          # FastAPI app
│   ├── alembic/             # Database migrations
│   ├── requirements.txt     # Python dependencies
│   └── Dockerfile           # Backend container
├── FRONTEND/
│   ├── src/
│   │   ├── components/      # Reusable UI components
│   │   ├── hooks/           # React Query hooks
│   │   ├── lib/             # API client, utilities
│   │   ├── pages/           # 18 page components
│   │   └── types/           # TypeScript types
│   └── package.json         # Node dependencies
├── Dockerfile               # Multi-stage build (frontend + backend)
├── render.yaml              # Render deployment config
└── docker-compose.yml       # Local development
```
