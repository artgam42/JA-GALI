"""
JA-GALI — Faz 6.2/6.3 : Rasanble done + Jenere rapò ak Claude

Konpile yon rezime peryòd (pwojè, revni, depans, payroll) apati
Journal Sheets la, epi mande Claude ekri yon rapò byen estriktire.

⚠️ jenere_rapò_ak_claude() BEZWEN KREDI API CLAUDE — menm depandans
ak Faz 1.5/5.3. rasanble_done_rapò() li menm PA bezwen Claude, li ka
teste san kredi (li Sheets sèlman).
"""

import os
import re
from datetime import date, datetime, timedelta

_PATÈN_KÒD = re.compile(r"^(PW\d{2}-\d{3,4}-[A-Za-z]|JA-[PC]\d{3}-\d{3,4}[A-Za-z])")


def rasanble_done_rapò(mwa_kont: int = 3) -> dict:
    """
    Li Journal Sheets la, filtre pa peryòd (dènye N mwa), konpile:
        - kantite pwojè inik (kòd ki kòmanse ak PW/JA-P/JA-C)
        - total revni, total depans, benefis net
        - rezime payroll pa kolaboratè (reyitilize payroll.py)

    Retounen yon dict done BRIT — Claude ap fòmate yo an rapò tèks.
    """
    from sheets_service import li_valè_brit
    from payroll import rezime_payroll
    from dat_util import pars_dat

    # Itilize valè BRIT (UNFORMATTED_VALUE) pou tout ranje a, sa jere
    # kòrèkteman dat ki estoke kòm vrè tip "date" nan Sheets la (nimewo
    # seri), ki pa ta pase ak yon senp li_liy() tèks fòmate.
    liy_yo = li_valè_brit("A:G")

    if not liy_yo or len(liy_yo) <= 1:
        return {
            "mwa_kont": mwa_kont,
            "kantite_pwoje": 0,
            "total_revni": 0.0,
            "total_depans": 0.0,
            "benefis_net": 0.0,
            "payroll": {},
        }

    jodi = date.today()
    limit_dat = jodi - timedelta(days=30 * mwa_kont)

    kòd_yo_vi = set()
    total_revni = 0.0
    total_depans = 0.0

    for liy in liy_yo[1:]:
        if not liy:
            continue

        dat_obj = pars_dat(liy[0] if len(liy) > 0 else None)
        if dat_obj is None or dat_obj < limit_dat:
            continue

        type_operat = str(liy[1]).strip().lower() if len(liy) > 1 else ""
        description = str(liy[4]).strip() if len(liy) > 4 else ""

        try:
            payer = float(liy[6]) if len(liy) > 6 and liy[6] not in ("", None) else 0.0
        except (ValueError, TypeError):
            payer = 0.0

        if type_operat == "revni":
            total_revni += payer
        elif type_operat == "depans":
            total_depans += payer

        m = _PATÈN_KÒD.match(description)
        if m:
            kòd_yo_vi.add(m.group(1).upper())

    payroll_rezilta = rezime_payroll(mwa_kont=mwa_kont)

    return {
        "mwa_kont": mwa_kont,
        "kantite_pwoje": len(kòd_yo_vi),
        "total_revni": round(total_revni, 2),
        "total_depans": round(total_depans, 2),
        "benefis_net": round(total_revni - total_depans, 2),
        "payroll": payroll_rezilta.get("data", {}),
    }


def jenere_rapò_ak_claude(done: dict) -> str:
    """
    Voye done rasanble yo (tèks sèlman, pa gen imaj) bay Claude, mande
    l ekri yon rapò byen estriktire an Kreyòl.
    """
    from anthropic import Anthropic

    kle = os.getenv("ANTHROPIC_API_KEY")
    modèl = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-6")
    client = Anthropic(api_key=kle)

    if done["payroll"]:
        payroll_tèks = "\n".join(
            f"  - {non}: {montan} goud" for non, montan in done["payroll"].items()
        )
    else:
        payroll_tèks = "  (pa gen done payroll pou peryòd sa a)"

    prompt = (
        f"Ekri yon rapò biznis pwofesyonèl an Kreyòl ayisyen pou ajans JUST ART, "
        f"ki kouvri dènye {done['mwa_kont']} mwa yo. Itilize done sa yo:\n\n"
        f"- Kantite pwojè reyalize: {done['kantite_pwoje']}\n"
        f"- Total revni: {done['total_revni']} goud\n"
        f"- Total depans: {done['total_depans']} goud\n"
        f"- Benefis net: {done['benefis_net']} goud\n"
        f"- Rezime payroll pa kolaboratè:\n{payroll_tèks}\n\n"
        f"Estriktire rapò a ak yon tit, yon ti entwodiksyon, seksyon separe pou "
        f"chak kategori done, ak yon konklizyon kout. Rete pwofesyonèl e klè."
    )

    repons = client.messages.create(
        model=modèl,
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}],
    )

    return repons.content[0].text


def jenere_epi_kreye_rapò(mwa_kont: int = 3) -> dict:
    """
    Woutin konplè Faz 6 (VÈSYON GOOGLE DOCS — pa itilize ankò, gade
    jenere_rapò_pdf() pou vèsyon aktyèl la ki itilize PDF olye Docs,
    akoz limitasyon kota depo service account sou kont Google pèsonèl).

    Kite fonksyon sa a pou referans si w vin gen Google Workspace pita.
    """
    from docs_service import kreye_rapò

    done = rasanble_done_rapò(mwa_kont)
    tèks_rapò = jenere_rapò_ak_claude(done)

    jodi = date.today().strftime("%d-%m-%Y")
    tit = f"Rapò JUST ART — {jodi} (dènye {mwa_kont} mwa)"

    rezilta_doc = kreye_rapò(tit, tèks_rapò)

    return {
        "tit": tit,
        "lyen": rezilta_doc["lyen"],
        "done": done,
    }


def jenere_rapò_pdf(mwa_kont: int = 3) -> tuple:
    """
    Woutin konplè Faz 6 (VÈSYON PDF — aktyèl): rasanble done → jenere
    tèks ak Claude → konstwi yon fichye PDF, san pase pa Google Docs
    (evite limitasyon kota service account sou kont Google pèsonèl).

    Retounen (pdf_byt: bytes, tit: str).
    """
    done = rasanble_done_rapò(mwa_kont)
    tèks_rapò = jenere_rapò_ak_claude(done)

    jodi = date.today().strftime("%d-%m-%Y")
    tit = f"Rapò JUST ART - {jodi} (dènye {mwa_kont} mwa)"

    pdf_byt = _kreye_pdf(tit, tèks_rapò)

    return pdf_byt, tit


def _fòmate_tèks_senp(done: dict) -> str:
    """
    Fòmate done yo an tèks lizib SAN Claude — itil pou teste chèn
    Sheets → PDF la san bezwen kredi API. Mwens elegant pase vèsyon
    Claude a, men montre menm done reyèl yo.
    """
    if done["payroll"]:
        payroll_tèks = "\n".join(
            f"  - {non}: {montan} goud" for non, montan in done["payroll"].items()
        )
    else:
        payroll_tèks = "  (pa gen done payroll pou peryòd sa a)"

    return (
        f"Rapò otomatik pou dènye {done['mwa_kont']} mwa yo.\n\n"
        f"RESIME FINANSYE\n"
        f"----------------\n"
        f"Kantite pwojè reyalize: {done['kantite_pwoje']}\n"
        f"Total revni: {done['total_revni']} goud\n"
        f"Total depans: {done['total_depans']} goud\n"
        f"Benefis net: {done['benefis_net']} goud\n\n"
        f"PAYROLL PA KOLABORATÈ\n"
        f"----------------------\n"
        f"{payroll_tèks}\n\n"
        f"(Rapò sa a fòmate ak tèks senp, san Claude — pou tès Faz 6 "
        f"san kredi API. Vèsyon final la ap pi byen ekri, jenere pa Claude.)"
    )


def jenere_rapò_pdf_san_claude(mwa_kont: int = 3) -> tuple:
    """
    Menm jan ak jenere_rapò_pdf(), men SAN apèl Claude — itilize
    _fòmate_tèks_senp() olye jenere_rapò_ak_claude(). Pèmèt teste
    tout chèn Sheets → PDF san bezwen kredi API Claude.

    Retounen (pdf_byt: bytes, tit: str).
    """
    done = rasanble_done_rapò(mwa_kont)
    tèks_rapò = _fòmate_tèks_senp(done)

    jodi = date.today().strftime("%d-%m-%Y")
    tit = f"Rapò TES (san Claude) - {jodi} (denye {mwa_kont} mwa)"

    pdf_byt = _kreye_pdf(tit, tèks_rapò)

    return pdf_byt, tit


def _sanitize_pou_pdf(tèks: str) -> str:
    """
    Fonn PDF estanda yo (Helvetica) sèlman sipòte Latin-1 — karaktè
    aksan Kreyòl (è, ò, à, ù, é) OK, men tirè long (—), guillemè, ak
    emoji PA sipòte. Ranplase yo ak ekivalan ASCII, epi pwoteje kont
    nenpòt lòt karaktè ki rete pa sipòte (ranplase ak '?').
    """
    ranplasman = {
        "\u2014": "-",   # tirè long (em dash)
        "\u2013": "-",   # tirè mwayen (en dash)
        "\u2018": "'", "\u2019": "'",
        "\u201c": '"', "\u201d": '"',
        "\u2026": "...",
        "•": "-",
    }
    for kle, valè in ranplasman.items():
        tèks = tèks.replace(kle, valè)

    return tèks.encode("latin-1", errors="replace").decode("latin-1")


def _kreye_pdf(tit: str, tèks: str) -> bytes:
    """Konstwi yon fichye PDF senp ak tit + kò tèks, retounen byt li."""
    from fpdf import FPDF

    tit = _sanitize_pou_pdf(tit)
    tèks = _sanitize_pou_pdf(tèks)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.multi_cell(0, 10, tit)
    pdf.ln(4)
    pdf.set_font("Helvetica", size=11)
    pdf.multi_cell(0, 7, tèks)

    sòti = pdf.output()
    return bytes(sòti)
