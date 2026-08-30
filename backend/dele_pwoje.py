"""
JA-GALI — Faz 4.2 : Kòmand "delè pou KÒD se DAT" (SAN Claude)

Egzanp mesaj ki dwe rekonèt:
    "delè pou PW26-816-A se 28/08/2026"
    "PW26-816-A delè 28/08/2026"
    "JA-P005-701A delè: 05/09/2026"

Fòma dat egzije: JJ/MM/AAAA (konsistan ak rès sistèm nan).
"""

import re
from datetime import date, datetime
from typing import Optional

_PATÈN_KÒD_PWOJE = re.compile(
    r"\b(PW\d{2}-\d{3,4}-[A-Za-z]|JA-[PC]\d{3}-\d{3,4}[A-Za-z])\b",
    re.IGNORECASE,
)

_MO_KLE_DELÈ = re.compile(r"\bd[èe]l[èe]\b", re.IGNORECASE)

_PATÈN_DAT = re.compile(r"\b(\d{1,2})/(\d{1,2})/(\d{4})\b")


def detekte_kòmand_delè(mesaj: str) -> Optional[dict]:
    """
    Analize yon mesaj pou wè si li se yon kòmand "delè pou KÒD se DAT".

    Retounen {"kòd": str, "dat": date} si rekonèt, None otreman.
    """
    if not mesaj or not mesaj.strip():
        return None

    kòd_matche = _PATÈN_KÒD_PWOJE.search(mesaj)
    delè_matche = _MO_KLE_DELÈ.search(mesaj)
    dat_matche = _PATÈN_DAT.search(mesaj)

    if not (kòd_matche and delè_matche and dat_matche):
        return None

    jou, mwa, ane = dat_matche.groups()
    try:
        dat_obj = date(int(ane), int(mwa), int(jou))
    except ValueError:
        return None  # dat envalid (egzanp 32/13/2026)

    return {"kòd": kòd_matche.group(1).upper(), "dat": dat_obj}


def pwosè_kòmand_delè(mesaj: str) -> dict:
    """
    Woutin konplè: detekte kòmand la, kreye evènman Calendar la.

    Retounen {"rekonèt": bool, "kòd", "dat", "event_id", "estati"}.
    """
    rezilta_deteksyon = detekte_kòmand_delè(mesaj)

    if rezilta_deteksyon is None:
        return {
            "rekonèt": False,
            "kòd": None,
            "dat": None,
            "event_id": None,
            "estati": "Mesaj la pa sanble ak yon kòmand 'delè' valid (fòma: JJ/MM/AAAA).",
        }

    from calendar_service import ajoute_delè_pwoje

    kòd = rezilta_deteksyon["kòd"]
    dat_delè = rezilta_deteksyon["dat"]

    event_id = ajoute_delè_pwoje(kòd, dat_delè)

    return {
        "rekonèt": True,
        "kòd": kòd,
        "dat": dat_delè.isoformat(),
        "event_id": event_id,
        "estati": f"✅ Delè pou '{kòd}' ({dat_delè.strftime('%d/%m/%Y')}) ajoute sou Calendar.",
    }
