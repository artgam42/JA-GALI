"""
JA-GALI — Faz 3.2/3.3 : Kòmand "delè pou X se DATE"

Rekonèt de kalite kòmand:
    1. Pwojè:  "delè pou PW26-816-A se 28/08/2026"
    2. Tach jenerik (egzanp piblikasyon): "delè pou piblikasyon Kafe Lakay se 25/08/2026"

Si mesaj la gen yon kòd pwojè valid, l ap trete kòm delè yon pwojè.
Otreman, tèks ant "pou" ak "se" a sèvi kòm tit yon evènman jenerik.

Fòma dat egzije: JJ/MM/AAAA.
"""

import re
from datetime import date
from typing import Optional

_PATÈN_KÒD_PWOJE = re.compile(
    r"\b(PW\d{2}-\d{3,4}-[A-Za-z]|JA-[PC]\d{3}-\d{3,4}[A-Za-z])\b",
    re.IGNORECASE,
)

_MO_KLE_DELÈ = re.compile(r"\bd[èe]l[èe]\b", re.IGNORECASE)

_PATÈN_DAT = re.compile(r"\b(\d{1,2})/(\d{1,2})/(\d{4})\b")

# Kaptire tit lib ant "pou" ak "se [dat]" — pou tach ki PA gen kòd pwojè
_PATÈN_TIT_JENERIK = re.compile(
    r"d[èe]l[èe]\s+pou\s+(.+?)\s+se\s+\d{1,2}/\d{1,2}/\d{4}",
    re.IGNORECASE,
)


def detekte_kòmand_delè(mesaj: str) -> Optional[dict]:
    """
    Analize yon mesaj pou wè si li se yon kòmand "delè pou X se DATE".

    Retounen:
        {"kalite": "pwojè", "kòd": str, "dat": date}   — si gen kòd pwojè
        {"kalite": "tach", "tit": str, "dat": date}    — si se yon tach jenerik
        None — si mesaj la pa matche fòma a ditou
    """
    if not mesaj or not mesaj.strip():
        return None

    delè_matche = _MO_KLE_DELÈ.search(mesaj)
    dat_matche = _PATÈN_DAT.search(mesaj)

    if not (delè_matche and dat_matche):
        return None

    jou, mwa, ane = dat_matche.groups()
    try:
        dat_obj = date(int(ane), int(mwa), int(jou))
    except ValueError:
        return None  # dat envalid (egzanp 32/13/2026)

    # 1. Priyorite: si gen yon kòd pwojè valid, se sa
    kòd_matche = _PATÈN_KÒD_PWOJE.search(mesaj)
    if kòd_matche:
        return {"kalite": "pwojè", "kòd": kòd_matche.group(1).upper(), "dat": dat_obj}

    # 2. Otreman, chèche yon tit jenerik ant "pou" ak "se"
    tit_matche = _PATÈN_TIT_JENERIK.search(mesaj)
    if tit_matche:
        tit = tit_matche.group(1).strip()
        if tit:
            return {"kalite": "tach", "tit": tit, "dat": dat_obj}

    return None


def pwosè_kòmand_delè(mesaj: str) -> dict:
    """
    Woutin konplè: detekte kòmand la, kreye evènman Calendar ki koresponn
    (swa lye ak yon kòd pwojè, swa yon evènman jenerik).

    Retounen {"rekonèt": bool, "kalite", "dat", "event_id", "estati", ...}.
    """
    rezilta_deteksyon = detekte_kòmand_delè(mesaj)

    if rezilta_deteksyon is None:
        return {
            "rekonèt": False,
            "estati": (
                "Mesaj la pa sanble ak yon kòmand 'delè' valid. Egzanp: "
                "'delè pou PW26-816-A se 28/08/2026' oswa "
                "'delè pou piblikasyon Kafe Lakay se 28/08/2026'."
            ),
        }

    dat_delè = rezilta_deteksyon["dat"]

    if rezilta_deteksyon["kalite"] == "pwojè":
        from calendar_service import ajoute_delè_pwoje

        kòd = rezilta_deteksyon["kòd"]
        event_id = ajoute_delè_pwoje(kòd, dat_delè)

        return {
            "rekonèt": True,
            "kalite": "pwojè",
            "kòd": kòd,
            "dat": dat_delè.isoformat(),
            "event_id": event_id,
            "estati": f"✅ Delè pou '{kòd}' ({dat_delè.strftime('%d/%m/%Y')}) ajoute sou Calendar.",
        }

    else:  # kalite == "tach"
        from calendar_service import kreye_evènman

        tit = rezilta_deteksyon["tit"]
        tit_evènman = f"📌 {tit}"
        event_id = kreye_evènman(tit_evènman, dat_delè, f"Tach: {tit}")

        return {
            "rekonèt": True,
            "kalite": "tach",
            "tit": tit,
            "dat": dat_delè.isoformat(),
            "event_id": event_id,
            "estati": f"✅ Tach '{tit}' ({dat_delè.strftime('%d/%m/%Y')}) ajoute sou Calendar.",
        }
