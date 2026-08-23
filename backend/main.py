"""
JA-GALI Backend — Asistan AI JUST ART
Faz 0.5 — Sèvè FastAPI debaz.

Sa a se fondasyon an. Woutt yo (routes) pou pwojè, peman, elatriye
ap vin ajoute nan Faz 1+.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(
    title="JA-GALI API",
    description="Backend pou Asistan AI JUST ART",
    version="0.1.0",
)

# CORS — pèmèt PWA a (ki ka sou yon lòt domèn/pò) rele API a.
# Nan Faz 6 (deplwaman), ranplase "*" ak vrè domèn PWA a pou plis sekirite.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def rasin():
    """Woutt tès senp pou konfime sèvè a ap kouri."""
    return {
        "sèvis": "JA-GALI Backend",
        "estati": "ap kouri",
        "faz": "0 — Fondasyon",
    }


@app.get("/sante")
def verifye_sante():
    """
    Woutt 'health check' — verifye si eleman kritik yo konfigire
    (pa egzanp: èske kle API Claude a prezan nan anviwonman an).
    """
    kle_claude_prezan = bool(os.getenv("ANTHROPIC_API_KEY"))

    return {
        "sèvè": "ok",
        "kle_claude_konfigire": kle_claude_prezan,
    }
