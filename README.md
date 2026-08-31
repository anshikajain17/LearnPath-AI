# LearnPath AI Next

An adaptive career-intelligence platform that turns a learner's goal, current skills, time budget and assessment evidence into an explainable, prerequisite-aware roadmap.

## What is upgraded

- Premium responsive React/Vite dashboard
- Career readiness score
- Interactive skill/dependency graph
- Adaptive roadmap regeneration after assessments
- Explainable recommendation scoring
- AI Coach with optional OpenAI integration; works in deterministic local mode without an API key
- Resume text/PDF upload and skill extraction
- Target-role gap analysis
- Project recommendations
- Smart weekly study schedule
- SQLite persistence through FastAPI
- API documentation via FastAPI
- Health endpoint
- Backend tests
- Dockerfiles for frontend and backend
- Render deployment blueprint

## Stack

Frontend: React, Vite, Lucide React, Recharts
Backend: FastAPI, Pydantic, SQLite, scikit-learn, PyPDF
AI: optional OpenAI-compatible provider; deterministic fallback when no key is configured

## Run in VS Code

### Backend (Windows PowerShell)

```powershell
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload --port 8000
```

### Frontend

Open another terminal:

```powershell
cd frontend
npm install
npm run dev
```

Open the Vite URL, normally http://localhost:5173.

## Optional AI

Copy `.env.example` to `.env` and add:

```env
OPENAI_API_KEY=your_key
OPENAI_MODEL=gpt-4.1-mini
```

The application still works without a key. The local AI Coach uses the learner's actual roadmap/profile rather than pretending a remote model was called.

## Tests

```powershell
cd backend
pytest -q
```

## Production deployment

### Backend
Deploy `backend` to a Python host such as Render/Railway/Fly.io.

Start command:

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### Frontend
Build:

```bash
npm run build
```

Serve the generated `frontend/dist` on Vercel/Netlify/Render static hosting.

Set:

```env
VITE_API_URL=https://YOUR-BACKEND-DOMAIN
```

For a one-click Render starting point, see `render.yaml`.

## Demo flow

1. Open the dashboard.
2. Set goal to: `Become an AI Engineer in 6 months. I know Python and basic ML. I can study 2 hours a day.`
3. Generate plan.
4. Show readiness, skill graph and roadmap.
5. Submit an assessment for Python/ML.
6. Regenerate the roadmap and show the changed next-best action.
7. Upload a resume or paste resume text.
8. Show target-role gaps.
9. Ask the AI Coach: `Why is Deep Learning recommended next?`
10. Show the weekly schedule and project recommendation.

## Important

This is designed as an original upgraded implementation rather than an untouched copy of the reference repository. Review third-party licenses and replace/demo assets according to your team's ownership and submission rules.
