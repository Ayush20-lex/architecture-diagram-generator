"""
Automated Architecture Diagram Generator - Backend
----------------------------------------------------
FastAPI service that accepts a plain-English architecture description,
sends it to Gemini with a strict system prompt, and returns clean
Mermaid.js diagram syntax for the frontend to render.

Run with:
    uvicorn main:app --reload --port 8000
"""

import os
import re
import logging
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

import groq

# --------------------------------------------------------------------------
# Config
# --------------------------------------------------------------------------

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("diagram-generator")

def load_local_env() -> None:
    """Load KEY=value pairs from backend/.env for local development."""
    env_path = Path(__file__).with_name(".env")
    if not env_path.exists():
        return

    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip("\"'"))


load_local_env()

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
MODEL_NAME = os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile")

if not GROQ_API_KEY:
    logger.warning(
        "GROQ_API_KEY is not set. Set it as an environment variable "
        "before making requests, e.g. PowerShell: `$env:GROQ_API_KEY='your-key'`"
    )

client = groq.Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

SYSTEM_PROMPT = """You are an expert software architect and Mermaid.js diagram generator.

Given a plain-English description of a system's architecture, produce ONLY valid Mermaid.js
diagram syntax that visually represents it.

Rules you MUST follow:
1. Output ONLY the raw Mermaid code. No explanations, no commentary, no markdown code fences
   (no ```mermaid or ```), no leading/trailing text of any kind.
2. Choose the most appropriate diagram type for the description (usually `flowchart TD` or
   `flowchart LR` for architecture diagrams, but use `sequenceDiagram`, `classDiagram`, or
   `erDiagram` if the description clearly calls for it).
3. Use short, valid, unique node IDs (e.g. A, B, C or client, api, db) and put human-readable
   labels in square brackets or parentheses as appropriate for the diagram type.
4. Group related nodes using `subgraph` blocks where it improves clarity (e.g. "Frontend",
   "Backend", "Data Layer").
5. Use directional arrows (-->) to show data/request flow. To label an edge, use the format `A -- "Label Text" --> B`. DO NOT use `|>` or other invalid arrow types.
6. Keep the diagram readable: avoid overly dense graphs, avoid special characters that break
   Mermaid parsing (no unescaped quotes or parentheses inside labels).
7. The output must be syntactically valid Mermaid.js that renders with zero errors.

Respond with the Mermaid syntax only."""


# --------------------------------------------------------------------------
# App setup
# --------------------------------------------------------------------------

app = FastAPI(title="Architecture Diagram Generator API")

# CORS: allow the local frontend (and any origin during local dev) to call this API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For local dev. Restrict this to your frontend's origin in production.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class DiagramRequest(BaseModel):
    description: str = Field(..., min_length=1, max_length=8000)


class DiagramResponse(BaseModel):
    mermaid_code: str


def clean_mermaid_output(raw_text: str) -> str:
    """Strip markdown code fences or stray commentary if the model adds them anyway."""
    text = raw_text.strip()

    # Remove ```mermaid ... ``` or ``` ... ``` fences if present.
    fence_match = re.search(r"```(?:mermaid)?\s*(.*?)```", text, re.DOTALL)
    if fence_match:
        text = fence_match.group(1).strip()

    return text


@app.get("/health")
def health_check():
    return {"status": "ok", "model": MODEL_NAME, "api_key_configured": bool(GROQ_API_KEY)}


@app.post("/generate", response_model=DiagramResponse)
def generate_diagram(payload: DiagramRequest):
    if client is None:
        raise HTTPException(
            status_code=500,
            detail="Server is missing GROQ_API_KEY. Set it as an environment variable and restart the server.",
        )

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Architecture description:\n\n{payload.description}"}
            ],
            max_tokens=2000,
            temperature=0.1
        )
        raw_text = response.choices[0].message.content or ""

        mermaid_code = clean_mermaid_output(raw_text)

        if not mermaid_code:
            raise HTTPException(status_code=502, detail="Model returned an empty diagram.")

        return DiagramResponse(mermaid_code=mermaid_code)

    except Exception as e:
        logger.exception("Unexpected error generating diagram")
        raise HTTPException(status_code=502, detail=f"LLM API error: {str(e)}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
