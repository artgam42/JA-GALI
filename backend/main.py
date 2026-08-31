"""
JA-GALI Backend — Asistan AI JUST ART
Faz 0.5 — Sèvè FastAPI debaz.
Faz 1.1 — Woutt /chat debaz.

Sa a se fondasyon an. Woutt yo (routes) pou pwojè, peman, elatriye
ap vin ajoute nan Faz 1+.
"""

# pyrefly: ignore [missing-import]
from fastapi import Depends, FastAPI, Header, HTTPException
# pyrefly: ignore [missing-import]
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv
import os
import re

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

    # 0bis. Detekte "lis solde" — montre pwojè ki gen rès pou peye
    if re.search(r"\blis\s+solde\b", mesaj.message, re.IGNORECASE):
        from peman import lis_solde_yo
        try:
            solde_yo = lis_solde_yo(mwa_kont=3)
            if not solde_yo:
                return RepònsChat(
                    response="✅ Pa gen okenn solde k ap tann pou dènye 3 mwa yo."
                )
            liy_tèks = "\n".join(
                f"• {s['kliyan']} — {s['kòd']} : {s['rès']} goud"
                for s in solde_yo
            )
            return RepònsChat(
                response=f"💰 Solde k ap tann (dènye 3 mwa):\n\n{liy_tèks}"
            )
        except Exception as e:
            return RepònsChat(response=f"⚠️ Erè pandan chèche lis solde: {e}")

    # ── Detekte Kòmand Peman ak Depans (Faz 3) ───────────────────────
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

    # 3. Detekte Delè (Faz 4.2): "delè pou [kòd] se [JJ/MM/AAAA]"
    from dele_pwoje import detekte_kòmand_delè, pwosè_kòmand_delè

    if detekte_kòmand_delè(mesaj.message) is not None:
        try:
            rezilta = pwosè_kòmand_delè(mesaj.message)
            return RepònsChat(response=rezilta["estati"])
        except Exception as e:
            return RepònsChat(response=f"⚠️ Erè pandan ajoute delè sou Calendar: {e}")

    # 4. Detekte Caption (Faz 5.3): "caption pou [non piblikasyon]"
    patèn_caption = re.compile(r"(?:jenere\s+)?caption\s+pou\s+(.+)", re.IGNORECASE)
    match_caption = patèn_caption.search(mesaj.message)
    if match_caption:
        from caption_service import genere_caption
        try:
            non_pib = match_caption.group(1).strip()
            rezilta = genere_caption(non_pib)
            return RepònsChat(
                response=f"📝 Caption pou '{rezilta['non']}' "
                f"({rezilta['kantite_imaj']} imaj jwenn):\n\n{rezilta['caption']}"
            )
        except Exception as e:
            return RepònsChat(response=f"⚠️ Erè pandan jenerasyon caption: {e}")

    # 5. Otreman: kreyasyon nouvo pwojè (Faz 1.5/1.6, ekstraksyon Claude)
    from kreyasyon_pwoje import pwosè_nouvo_pwoje

    try:
        repons_kreyasyon = pwosè_nouvo_pwoje(mesaj.message)
        return RepònsChat(response=repons_kreyasyon)
    except Exception as e:
        return RepònsChat(response=f"⚠️ Erè pandan kreyasyon pwojè a: {e}")


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


@app.get("/alèt")
def get_alèt(jou: int = 30, _: None = Depends(verifye_kòd_aksè)):
    """
    Faz 4.4 — Woutt ki retounen evènman Calendar k ap pwoche pou
    montre nan paj "Alèt" PWA a.
    """
    from calendar_service import lis_evènman_k_ap_pwoche
    try:
        evènman_yo = lis_evènman_k_ap_pwoche(jou_alavans=jou)
        return {"evènman": evènman_yo}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/rapò")
def post_rapò(mwa: int = 3, _: None = Depends(verifye_kòd_aksè)):
    """
    Faz 6.4 — Woutt ki jenere yon rapò PDF (Sheets → Claude → PDF)
    epi retounen fichye a dirèkteman pou telechajman. Deklannche pa
    bouton "Jenere Rapò" PWA a.
    """
    # pyrefly: ignore [missing-import]
    from fastapi.responses import Response
    from rapo_service import jenere_rapò_pdf

    try:
        pdf_byt, tit = jenere_rapò_pdf(mwa_kont=mwa)
        non_fichye = f"{tit}.pdf".replace(" ", "_")
        return Response(
            content=pdf_byt,
            media_type="application/pdf",
            headers={"Content-Disposition": f'attachment; filename="{non_fichye}"'},
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class KòAksepteCaption(BaseModel):
    """Kò mesaj lè itilizatè a aksepte yon caption."""

    non_piblikasyon: str
    caption: str


@app.post("/caption/aksepte")
def post_aksepte_caption(kò: KòAksepteCaption, _: None = Depends(verifye_kòd_aksè)):
    """
    Faz 5.4 (amelyorasyon) — Lè itilizatè a klike "Aksepte" sou yon
    caption nan PWA a, ekri caption final la nan kolòn "Caption" nan
    Notion (menm liy ak piblikasyon an).
    """
    from notion_service import mete_ajou_caption

    try:
        mete_ajou_caption(kò.non_piblikasyon, kò.caption)
        return {"siksè": True, "mesaj": "Caption anrejistre nan Notion."}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



