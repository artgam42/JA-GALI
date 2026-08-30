"""
JA-GALI — Itilite pataje pou analize dat Google Sheets

Google Sheets ka retounen valè dat yo diferan fason selon ki mòd nou
li yo:
    - Nimewo SERI (ak valueRenderOption='UNFORMATTED_VALUE' epi selil
      la gen yon vrè tip "date") — jou depi 30 desanm 1899 (epòk
      Google Sheets).
    - Tèks fòmate (ak li_liy() nòmal) — fòma a varye selon paramèt
      rejyonal Sheet la (JJ/MM/AAAA, AAAA-MM-JJ, MM/JJ/AAAA, elatriye).

Fonksyon pars_dat() jere TOU DE ka yo, epi eseye plizyè fòma tèks
komen — pou n pa pèdi liy done akoz yon sèl fòma dat inatandi.
"""

from datetime import date, datetime, timedelta
from typing import Optional, Union

_EPOCH_SHEETS = datetime(1899, 12, 30)

_FÒMA_TÈKS = ("%d/%m/%Y", "%Y-%m-%d", "%m/%d/%Y", "%d-%m-%Y")


def pars_dat(valè: Union[str, int, float, None]) -> Optional[date]:
    """
    Konvèti yon valè dat Google Sheets (nimerik OSWA tèks) an yon
    objè date Python. Retounen None si valè a vid oswa pa rekonèt.
    """
    if valè is None or valè == "":
        return None

    # Ka 1: nimewo seri dirèk (Sheets UNFORMATTED_VALUE pou vrè dat)
    if isinstance(valè, (int, float)):
        try:
            return (_EPOCH_SHEETS + timedelta(days=float(valè))).date()
        except (ValueError, OverflowError, OSError):
            return None

    tèks = str(valè).strip()
    if not tèks:
        return None

    # Ka 2: tèks ki reprezante yon nimewo seri (egzanp "46261" oswa "46261.0")
    try:
        return (_EPOCH_SHEETS + timedelta(days=float(tèks))).date()
    except ValueError:
        pass

    # Ka 3: plizyè fòma tèks komen
    for fòma in _FÒMA_TÈKS:
        try:
            return datetime.strptime(tèks, fòma).date()
        except ValueError:
            continue

    return None
