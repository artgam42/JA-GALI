"""
JA-GALI — Faz 1.7 : Rekonesans kòmand "pwojè fini" (SAN Claude)

Poukisa san Claude: kòmand sa a gen yon fòma trè estriktire (yon kòd
pwojè + yon mo kle ki vle di "fini"). Yon senp rekonesans modèl (regex)
pi rapid, pi fyab, e li pa depann de kredi API.

Egzanp mesaj ki dwe rekonèt:
    "pwojè PW26-816-A fini"
    "PW26-816-A fin fèt"
    "JA-P005-701A konplete"
    "fini: JA-C004-620A"
"""

import re
from typing import Optional

# Rekonèt yon kòd pwojè valid, nenpòt kote li ye nan tèks la
_PATÈN_KÒD_PWOJE = re.compile(
    r"\b(PW\d{2}-\d{3,4}-[A-Za-z]|JA-[PC]\d{3}-\d{3,4}[A-Za-z])\b",
    re.IGNORECASE,
)

# Mo kle ki endike travay la fini
_MO_KLE_FINI = re.compile(
    r"\b(fini|fin\s+f[eè]t|konplete|complete|termine|done)\b",
    re.IGNORECASE,
)


def detekte_kòmand_fini(mesaj: str) -> Optional[str]:
    """
    Analize yon mesaj pou wè si li se yon kòmand "make pwojè fini".

    Retounen:
        Kòd pwojè a (an majiskil, fòma estanda) si mesaj la matche
        yon kòd VALID + yon mo kle "fini".
        None si mesaj la pa sanble ak yon kòmand konsa.
    """
    if not mesaj or not mesaj.strip():
        return None

    kòd_matche = _PATÈN_KÒD_PWOJE.search(mesaj)
    mo_kle_matche = _MO_KLE_FINI.search(mesaj)

    if kòd_matche and mo_kle_matche:
        return kòd_matche.group(1).upper()

    return None


def pwosè_kòmand_fini(mesaj: str) -> dict:
    """
    Woutin konplè pou tach 1.7: rekonèt kòmand la, epi chèche
    message_id Discord ki lye ak kòd la (nan onglè Discord_IDs).

    L'AKSYON edisyon Discord VRE a ap enplemante nan Faz 2, lè
    koneksyon Discord (webhook/bot) bati. Fonksyon sa a prepare tout
    enfo nesesè yo pou Faz 2 ka konekte san refè travay.

    Retounen yon dict:
        {"rekonèt": bool, "kòd": str|None, "message_id": str|None,
         "estati": str}
    """
    kòd = detekte_kòmand_fini(mesaj)

    if kòd is None:
        return {
            "rekonèt": False,
            "kòd": None,
            "message_id": None,
            "estati": "Mesaj la pa sanble ak yon kòmand 'pwojè fini' valid.",
        }

    # Enpòte isit (pa anlè fichye a) pou evite dependans sikilè ak
    # pou fasilite tès san Google Sheets konfigire.
    from sheets_service import jwenn_message_id

    message_id = jwenn_message_id(kòd)

    if message_id is None:
        return {
            "rekonèt": True,
            "kòd": kòd,
            "message_id": None,
            "estati": (
                f"Kòd '{kòd}' rekonèt, men pa gen mesaj Discord lye jwenn. "
                f"Verifye kòd la egzat, oswa pwojè a pa t kreye ak "
                f"notifikasyon Discord (Faz 2)."
            ),
        }

    return {
        "rekonèt": True,
        "kòd": kòd,
        "message_id": message_id,
        "estati": (
            f"Kòd '{kòd}' rekonèt, message_id '{message_id}' jwenn. "
            f"Pare pou edisyon Discord (⋯→FINI) — enplemante nan Faz 2."
        ),
    }
