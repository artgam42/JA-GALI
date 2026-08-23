"""
JA-GALI Backend — Asistan AI JUST ART
Faz 0.5 — Sèvè FastAPI debaz.
Faz 1.1 — Woutt /chat debaz.

Sa a se fondasyon an. Woutt yo (routes) pou pwojè, peman, elatriye
ap vin ajoute nan Faz 1+.
"""

from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(
    title="JA-GALI API",
    description="Backend pou Asistan AI JUST ART",
    version="0.1.0",
)

# CORS — pèmèt PWA a (ki ka sou yon lòt domèn/pò) rele API a.
# Nan Faz 7 (deplwaman), ranplase "*" ak vrè domèn PWA a pou plis sekirite.
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
        "faz": "1 — Backend debaz + Sheets + Premye PWA",
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


# ── Faz 1.2 — Otantifikasyon senp (yon sèl kòd pou tout ekip la) ────

def verifye_kòd_aksè(x_access_code: str = Header(default="")):
    """
    Dependency FastAPI ki verifye header 'X-Access-Code' anvan yon woutt
    pwoteje egzekite. Si kòd la pa matche sa ki nan .env (APP_ACCESS_CODE),
    voye yon erè 401.

    Itilizasyon: ajoute 'Depends(verifye_kòd_aksè)' nan paramèt yon woutt.
    """
    kòd_valid = os.getenv("APP_ACCESS_CODE")

    if not kòd_valid:
        # Pa gen kòd konfigire sou sèvè a — erè konfigirasyon, pa kite pase.
        raise HTTPException(
            status_code=500,
            detail="APP_ACCESS_CODE pa konfigire nan .env sèvè a.",
        )

    if x_access_code != kòd_valid:
        raise HTTPException(
            status_code=401,
            detail="Kòd aksè envalid. Verifye kòd ekip ou a.",
        )


# ── Faz 1.1 — Woutt /chat debaz ──────────────────────────────────────
#
# Etap sa a se yon SKÈLÈT sèlman: li resevwa yon mesaj epi retounen yon
# repons senp (echo), pou konfime kanal PWA ↔ backend la mache byen.
#
# Pwochèn etap yo ap vin GREFE sou woutt sa a:
#   - 1.2 : verifye kòd aksè anvan repons
#   - 1.5 : ranplase repons echo a ak vrè ekstraksyon Claude
#   - 1.6 : ekri liy nan Google Sheets apre ekstraksyon an


class MesajChat(BaseModel):
    """Kò (body) mesaj ki soti nan PWA a."""

    message: str


class RepònsChat(BaseModel):
    """Kò repons backend la voye tounen bay PWA a."""

    response: str


@app.post("/chat", response_model=RepònsChat)
def chat(mesaj: MesajChat, _: None = Depends(verifye_kòd_aksè)):
    """
    Woutt prensipal — resevwa yon mesaj an lang natirèl, retounen yon repons.
    Pwoteje pa kòd aksè (X-Access-Code header) — gade verifye_kòd_aksè().

    Faz 1.1 (kounye a): jis konfime mesaj la byen resevwa (echo).
    Faz 1.5 (pita): backend ap voye mesaj la bay Claude pou ekstraksyon
    done reyèl (kliyan, tip travay, elatriye) anvan l repons.
    """
    if not mesaj.message or not mesaj.message.strip():
        return RepònsChat(response="⚠️ Mesaj la vid — ekri yon kòmand.")

    return RepònsChat(
        response=f"✅ Mesaj resevwa: « {mesaj.message} » "
        f"(ekstraksyon Claude ap vin nan tach 1.5)"
    )

