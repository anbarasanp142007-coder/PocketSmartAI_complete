# PocketSmart AI

A complete FastAPI + Jinja2 implementation of the supplied PocketSmart AI specification.

Features:
- Home Interior Budget Planner
- Party Budget Planner
- Jewelry Budget Planner with optional outfit image
- Registration, login, logout and JWT
- Session info/data
- Recommendation history and details
- Gemini structured recommendations
- Deterministic catalog fallback when Gemini is unavailable
- Responsive HTML/CSS/JS frontend
- Automated tests

## Model compatibility

The supplied document specifies Gemini 1.5 Flash Pro. Google's current model catalog no longer lists that model, so this project defaults to the currently listed `gemini-3.8-flash`. Override `GEMINI_MODEL` in `.env` if your account exposes another supported model.

The code uses the current `google-genai` SDK, Pydantic structured output, and multimodal image parts.

## Run in VS Code

Windows PowerShell:
```powershell
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
python -m uvicorn app.main:app --reload
```

macOS/Linux:
```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python -m uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000

Swagger: http://127.0.0.1:8000/docs

For a no-key demo, set `USE_GEMINI=false`. The built-in catalog fallback still exercises all three planners.

Run tests:
```bash
pytest -q
```

## Real provider integrations

The specification names Amazon, Flipkart, IKEA, Swiggy, Zomato and OYO but supplies no API credentials/contracts. Therefore this implementation uses an explicit mock catalog with outbound platform links instead of claiming live prices or inventory. Replace `CatalogService.search()` with official provider API adapters when credentials are available.
