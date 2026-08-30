"""
JA-GALI — Faz 1.4 : Lojik kòd pwojè otomatik

Jenere kòd pwojè selon 3 kalite kliyan (gade Contexte.md §3.1):
    Regilye : PW[ane 2-chif]-[mwa][jou]-[lèt]      egzanp PW26-816-A
    Patnè   : JA-P[nimewo fiks]-[mwa][jou][lèt]    egzanp JA-P005-701A
    Kontra  : JA-C[nimewo fiks]-[mwa][jou][lèt]    egzanp JA-C004-620A

Nòt sou fòma dat la (MDD):
    - Mwa a PA gen zewo devan (mwa 8 → "8", pa "08")
    - Jou a TOUJOU 2 chif (jou 5 → "05")
    - Sa bay 3 chif pou mwa 1-9, 4 chif pou mwa 10-12
    - Egzanp: 16 out 2026 → "816"   |   3 oktòb 2026 → "1003"

Règ kle:
    - Lèt sekans (A, B, C...) depann de konbyen pwojè ki deja gen menm
      dat (+ menm nimewo si patnè/kontra) nan kòlòn Description a.
    - Nimewo Patnè/Kontra se FIKS, li soti nan partenaires_contrats.json
      (pa jenere otomatikman) — si kliyan an pa nan lis la, nou REFIZE.
    - Si estati kliyan an pa "aktif" (Stop/Rezilye/Non renouvle/Kontra
      rompu), nou AVÈTI men kontinye kreye pwojè a kanmenm.
"""

import json
import os
import re
from datetime import date
from typing import Literal, Optional

KaliteKliyan = Literal["regilye", "patnè", "kontra"]

CHEMEN_KONFIG = os.path.join(os.path.dirname(__file__), "partenaires_contrats.json")


class KliyanPaNanListeErreur(Exception):
    """Leve lè yon patnè/kontra mande yon kòd men li pa nan lis konfig la."""
    pass


# ── Fòmatè dat ────────────────────────────────────────────────────────


def _dat_yy(dat: date) -> str:
    """Ane sou 2 chif — egzanp 2026 → '26'."""
    return f"{dat.year % 100:02d}"


def _dat_mdd(dat: date) -> str:
    """
    Mwa (san zewo devan) + jou (2 chif toujou).
    Egzanp: 16 out → '816'   |   3 oktòb → '1003'
    """
    return f"{dat.month}{dat.day:02d}"


# ── Chajman konfig patnè/kontra ──────────────────────────────────────


def _chaje_konfig_patnè_kontra() -> dict:
    with open(CHEMEN_KONFIG, "r", encoding="utf-8") as f:
        return json.load(f)


def jwenn_nimewo_patnè_kontra(non_kliyan: str, kalite: KaliteKliyan) -> tuple[str, str]:
    """
    Chèche nimewo fiks yon patnè/kontra nan konfig la.

    Retounen: (nimewo, estati)
    Leve KliyanPaNanListeErreur si kliyan an pa jwenn nan lis la.
    """
    konfig = _chaje_konfig_patnè_kontra()
    kle_kategori = "patnè" if kalite == "patnè" else "kontra"
    lis = konfig.get(kle_kategori, {})

    non_nòmalize = non_kliyan.strip().upper()
    for non_konfig, enfo in lis.items():
        if non_konfig.strip().upper() == non_nòmalize:
            return enfo["nimewo"], enfo["estati"]

    raise KliyanPaNanListeErreur(
        f"'{non_kliyan}' pa jwenn nan lis {kle_kategori} yo. "
        f"Ajoute l manyèlman nan partenaires_contrats.json anvan ou kreye pwojè a."
    )


def detèmine_kalite_kliyan(non_kliyan: str) -> KaliteKliyan:
    """
    Detèmine kalite kliyan (patnè/kontra/regilye) an konsiltan lis
    konfig la, pa non kliyan an (san sansib majiskil/miniskil).

    Si non kliyan an pa jwenn nan ni lis patnè ni lis kontra, li
    konsidere kòm yon kliyan REGILYE pa default.
    """
    konfig = _chaje_konfig_patnè_kontra()
    non_nòmalize = non_kliyan.strip().upper()

    for non_konfig in konfig.get("patnè", {}):
        if non_konfig.strip().upper() == non_nòmalize:
            return "patnè"

    for non_konfig in konfig.get("kontra", {}):
        if non_konfig.strip().upper() == non_nòmalize:
            return "kontra"

    return "regilye"


# ── Parse kòd egziste nan Description pou konte sekans ──────────────
#
#   PW26-816-A : ...      → kliyan regilye : yy='26', mdd='816', lèt='A'
#   JA-P005-701A : ...    → patnè          : nimewo='005', mdd='701', lèt='A'
#   JA-C004-620A : ...    → kontra         : nimewo='004', mdd='620', lèt='A'

_PATÈN_REGILYE = re.compile(r"^PW(\d{2})-(\d{3,4})-([A-Za-z])\s*:")
_PATÈN_PATNÈ = re.compile(r"^JA-P(\d{3})-(\d{3,4})([A-Za-z])\s*:")
_PATÈN_KONTRA = re.compile(r"^JA-C(\d{3})-(\d{3,4})([A-Za-z])\s*:")


def _pwochen_lèt(lèt_itilize: set) -> str:
    """Retounen pwochen lèt disponib (A, B, C...) ki pa nan sa deja itilize."""
    for i in range(26):
        lèt = chr(ord("A") + i)
        if lèt not in lèt_itilize:
            return lèt
    raise ValueError("Plis pase 26 pwojè pou menm dat — ka sa a pa prevwa.")


def _konte_lèt_pou_regilye(deskripsyon_yo: list, yy: str, mdd: str) -> str:
    """Konte lèt sekans deja itilize pou yon dat kliyan regilye, retounen pwochen an."""
    lèt_itilize = set()
    for tèks in deskripsyon_yo:
        m = _PATÈN_REGILYE.match(str(tèks).strip())
        if m and m.group(1) == yy and m.group(2) == mdd:
            lèt_itilize.add(m.group(3).upper())
    return _pwochen_lèt(lèt_itilize)


def _konte_lèt_pou_patnè_kontra(
    deskripsyon_yo: list, patèn: "re.Pattern", nimewo: str, mdd: str
) -> str:
    """Konte lèt sekans deja itilize pou yon nimewo+dat patnè/kontra, retounen pwochen an."""
    lèt_itilize = set()
    for tèks in deskripsyon_yo:
        m = patèn.match(str(tèks).strip())
        if m and m.group(1) == nimewo and m.group(2) == mdd:
            lèt_itilize.add(m.group(3).upper())
    return _pwochen_lèt(lèt_itilize)


# ── Fonksyon prensipal ────────────────────────────────────────────────


def jenere_kòd(
    kalite_kliyan: KaliteKliyan,
    non_kliyan: str,
    deskripsyon_egziste: list,
    dat: Optional[date] = None,
) -> dict:
    """
    Jenere yon kòd pwojè konplè.

    Paramèt:
        kalite_kliyan: "regilye" | "patnè" | "kontra"
        non_kliyan: non kliyan an (itilize pou chèche nimewo si patnè/kontra)
        deskripsyon_egziste: lis tout valè kòlòn Description ki deja nan Sheets
                              (soti nan sheets_service.li_liy("E:E"))
        dat: dat pwojè a (default: jodi a)

    Retounen yon dict:
        {"kòd": "PW26-816-A", "avètisman": None oswa yon mesaj tèks}

    Leve KliyanPaNanListeErreur si se yon patnè/kontra ki pa nan lis la.
    """
    if dat is None:
        dat = date.today()

    avètisman = None
    mdd = _dat_mdd(dat)

    if kalite_kliyan == "regilye":
        yy = _dat_yy(dat)
        lèt = _konte_lèt_pou_regilye(deskripsyon_egziste, yy, mdd)
        kòd = f"PW{yy}-{mdd}-{lèt}"

    elif kalite_kliyan in ("patnè", "kontra"):
        nimewo, estati = jwenn_nimewo_patnè_kontra(non_kliyan, kalite_kliyan)

        if estati != "aktif":
            avètisman = (
                f"⚠️ Atansyon: '{non_kliyan}' gen estati '{estati}' "
                f"(pa aktif). Pwojè a ap kreye kanmenm."
            )

        prefiks = "P" if kalite_kliyan == "patnè" else "C"
        patèn = _PATÈN_PATNÈ if kalite_kliyan == "patnè" else _PATÈN_KONTRA

        lèt = _konte_lèt_pou_patnè_kontra(deskripsyon_egziste, patèn, nimewo, mdd)
        kòd = f"JA-{prefiks}{nimewo}-{mdd}{lèt}"

    else:
        raise ValueError(f"Kalite kliyan enkoni: '{kalite_kliyan}'")

    return {"kòd": kòd, "avètisman": avètisman}
