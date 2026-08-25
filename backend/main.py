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

    Lojik entèn (backend deside, PWA pa bezwen konnen detay yo):
      1. Si mesaj la vid → mesaj avètisman
      2. Si mesaj la matche yon kòmand "pwojè fini" (regex, san Claude,
         Faz 1.7) → trete l kòm sa, retounen estati a
      3. Otreman → echo pou kounye a (Faz 1.5 ap ranplase sa ak vrè
         ekstraksyon Claude)
    """
    if not mesaj.message or not mesaj.message.strip():
        return RepònsChat(response="⚠️ Mesaj la vid — ekri yon kòmand.")

    # Tès rapid san Sheets: si pa gen kòd+mo kle "fini" nan mesaj la,
    # pa menm eseye konekte ak Sheets — sa evite erè initil pou mesaj
    # nòmal (kreyasyon pwojè, elatriye).
    from estati_pwoje import detekte_kòmand_fini

    if detekte_kòmand_fini(mesaj.message) is not None:
        from estati_pwoje import pwosè_kòmand_fini
        from discord_service import edite_mesaj_fini_san_kraze

        try:
            rezilta = pwosè_kòmand_fini(mesaj.message)

            if rezilta["message_id"] is not None:
                reyisi = edite_mesaj_fini_san_kraze(
                    rezilta["kòd"], rezilta["message_id"]
                )
                if reyisi:
                    return RepònsChat(
                        response=f"✅ Pwojè '{rezilta['kòd']}' make FINI — mesaj Discord edite."
                    )
                else:
                    return RepònsChat(
                        response=f"⚠️ Pwojè '{rezilta['kòd']}' rekonèt men edisyon Discord echwe "
                        f"(verifye webhook konfigire nan .env)."
                    )

            return RepònsChat(response=rezilta["estati"])
        except Exception as e:
            return RepònsChat(
                response=f"⚠️ Erè pandan trete kòmand 'fini' a: {e}"
            )

    # ── Detekte Kòmand Peman ak Depans (Faz 3) ───────────────────────
    import re

    # 1. Detekte Peman: "peye [montan] pou [kòd]" oswa "peman [montan] [kòd]"
    patèn_peman = re.compile(
        r"\b(?:peye|peman)\s+(\d+(?:\.\d+)?)\s*(?:pou\s+)?(?:pwojè\s+)?\b(PW\d{2}-\d{3,4}-[A-Za-z]|JA-[PC]\d{3}-\d{3,4}[A-Za-z])\b",
        re.IGNORECASE
    )
    match_peman = patèn_peman.search(mesaj.message)
    if match_peman:
        from peman import ajoute_peman
        try:
            montan = float(match_peman.group(1))
            kòd = match_peman.group(2).upper()
            rezilta = ajoute_peman(kòd, montan)
            return RepònsChat(response=rezilta["mesaj"])
        except Exception as e:
            return RepònsChat(response=f"⚠️ Erè pandan anrejistreman peman an: {e}")

    # 2. Detekte Depans: "depans [montan] kategori [kategori] pou [non_depans] : [deskripsyon]"
    patèn_depans = re.compile(
        r"\bdepans\s+(\d+(?:\.\d+)?)\s+(?:kategori\s+)?(\w+)\s+(?:pou\s+)?([^:]+)(?::\s*(.+))?",
        re.IGNORECASE
    )
    match_depans = patèn_depans.search(mesaj.message)
    if match_depans:
        from depans import ajoute_depans
        try:
            montan = float(match_depans.group(1))
            kategori = match_depans.group(2)
            non_depans = match_depans.group(3).strip()
            deskripsyon = match_depans.group(4).strip() if match_depans.group(4) else non_depans
            
            rezilta = ajoute_depans(
                kategori=kategori,
                deskripsyon=deskripsyon,
                montan=montan,
                non_depans=non_depans
            )
            return RepònsChat(response=rezilta["mesaj"])
        except Exception as e:
            return RepònsChat(response=f"⚠️ Erè pandan anrejistreman depans lan: {e}")

    return RepònsChat(
        response=f"✅ Mesaj resevwa: « {mesaj.message} » "
        f"(ekstraksyon Claude ap vin nan tach 1.5)"
    )


@app.get("/payroll")
def get_payroll(mwa: int = 3, _: None = Depends(verifye_kòd_aksè)):
    """
    Woutt ki retounen rapò payroll kolaboratè yo pou dènye N mwa yo.
    """
    from payroll import rezime_payroll
    try:
        rezilta = rezime_payroll(mwa_kont=mwa)
        return rezilta
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



