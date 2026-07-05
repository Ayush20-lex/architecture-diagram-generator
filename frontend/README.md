# Architecture Diagram Generator

## Project structure
```
project/
├── backend/
│   ├── main.py
│   └── requirements.txt
└── frontend/
    └── index.html
```

## 1. Backend setup

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

export ANTHROPIC_API_KEY=sk-ant-...   # Windows (PowerShell): $env:ANTHROPIC_API_KEY="sk-ant-..."

uvicorn main:app --reload --port 8000
```

The API will be live at `http://localhost:8000`. Check `http://localhost:8000/health` to confirm the key is loaded.

To use Gemini instead, swap the `anthropic` client call in `main.py`'s `generate_diagram` function for the Gemini SDK equivalent — the rest of the FastAPI/CORS/response structure stays the same.

## 2. Frontend setup

No build step — it's a single static HTML file.

```bash
cd frontend
python -m http.server 5500
```

Open `http://localhost:5500` in your browser. (Opening `index.html` directly by double-clicking also works, since it just calls `http://localhost:8000` via fetch.)

## 3. Using it

1. Type or paste a plain-English architecture description in the left panel (or click one of the example chips).
2. Click **Generate Diagram** (or press Cmd/Ctrl+Enter).
3. The backend sends your description to Claude, gets back Mermaid syntax, and the frontend renders it live in the right-hand schematic pane.
4. Use **Copy Mermaid** to grab the raw syntax for reuse elsewhere (e.g. in a README or Notion doc).

## Notes

- CORS is wide open (`allow_origins=["*"]`) for local development. Restrict `allow_origins` to your actual frontend origin before deploying.
- If Mermaid fails to render (rare, but LLMs occasionally emit a syntax slip), the app shows an inline error and you can just click Generate again.
- Model is configurable via the `ANTHROPIC_MODEL` environment variable if you want to point at a different Claude model.
