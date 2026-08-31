"""
JA-GALI — Faz 2 : Notifikasyon Discord (Template Otomatik)

Fonksyon pou voye ak edite mesaj Discord atravè webhook, selon kalite
kliyan (regilye/patnè/kontra) — chak gen pwòp kanal/webhook.

⚠️ Mekanis edisyon: yon webhook Discord ka SÈLMAN edite mesaj LI MENM
te voye. Nou detèmine otomatikman ki webhook itilize apati fòma kòd
pwojè a (PW... = regilye, JA-P... = patnè, JA-C... = kontra) — pa gen
bezwen estoke enfo anplis pou sa.
"""

import os
import re
import requests
from typing import Literal, Optional

KaliteKliyan = Literal["regilye", "patnè", "kontra"]


class WebhookPaKonfigireErreur(Exception):
    """Leve lè yon webhook mande pa gen URL konfigire nan .env."""
    pass


# ── Detèmine kalite kliyan apati kòd pwojè a ─────────────────────────


def kalite_apati_kòd(kòd_pwoje: str) -> KaliteKliyan:
    """Detèmine kalite kliyan (regilye/patnè/kontra) apati fòma kòd la."""
    kòd = kòd_pwoje.strip().upper()
    if kòd.startswith("JA-P"):
        return "patnè"
    if kòd.startswith("JA-C"):
        return "kontra"
    if kòd.startswith("PW"):
        return "regilye"
    raise ValueError(f"Fòma kòd pwojè pa rekonèt: '{kòd_pwoje}'")


def _webhook_url(kalite: KaliteKliyan) -> str:
    """Jwenn URL webhook nan .env selon kalite kliyan."""
    kle_env = {
        "regilye": "DISCORD_WEBHOOK_REGILYE",
        "patnè": "DISCORD_WEBHOOK_PATNE",
        "kontra": "DISCORD_WEBHOOK_KONTRA",
    }[kalite]

    url = os.getenv(kle_env)
    if not url:
        raise WebhookPaKonfigireErreur(
            f"{kle_env} pa konfigire nan .env. "
            f"Gade Faz 2.1 nan fèy wout la pou kreye webhook Discord la."
        )
    return url


# ── Fòmatè template ───────────────────────────────────────────────────


def fòmate_template(
    kòd: str,
    type_travay: str,
    infos: str,
    delè: str,
    kolaboratè: str,
    statut: str = "⋯",
) -> str:
    """
    Konstwi tèks mesaj Discord la, fòma estanda:
        ● {kòd}
        - Type Travay : {type_travay}
        - Infos : {infos}
        - Delè : {delè}
        - Kolaboratè : {kolaboratè}
        - Statut : {statut}
    """
    return (
        f"● **{kòd}**\n"
        f"- Type Travay : {type_travay}\n"
        f"- Infos : {infos}\n"
        f"- Delè : {delè}\n"
        f"- Kolaboratè : {kolaboratè}\n"
        f"- Statut : {statut}"
    )


# ── Voye premye mesaj (Faz 2.2 / 2.3) ────────────────────────────────


def voye_notifikasyon_nouvo_pwoje(
    kòd: str,
    type_travay: str,
    infos: str,
    delè: str,
    kolaboratè: str,
) -> str:
    """
    Voye PREMYE mesaj Discord pou yon nouvo pwojè (statut = ⋯).

    Retounen: message_id Discord la (pou estoke, gade
    sheets_service.estoke_message_id).

    Leve WebhookPaKonfigireErreur oswa requests.HTTPError si echwe.
    """
    kalite = kalite_apati_kòd(kòd)
    url = _webhook_url(kalite)
    tèks = fòmate_template(kòd, type_travay, infos, delè, kolaboratè, statut="⋯")

    repons = requests.post(
        f"{url}?wait=true",
        json={"content": tèks},
        timeout=10,
    )
    repons.raise_for_status()

    return repons.json()["id"]


# ── Edite mesaj pou FINI (Faz 2.3bis / 1.7) ──────────────────────────


def edite_mesaj_fini(kòd: str, message_id: str) -> None:
    """
    Edite yon mesaj Discord ki deja egziste pou chanje Statut la nan
    ⋯ → FINI, AN KENBE tout rès tèks orijinal la (Type Travay, Infos,
    Delè, Kolaboratè). Sèlman liy Statut la chanje.

    Itilize GET pou rekipere mesaj orijinal la, ranplase sèlman liy
    "- Statut : ..." ladan l, epi PATCH tounen tèks konplè a.

    Leve WebhookPaKonfigireErreur oswa requests.HTTPError si echwe.
    """
    kalite = kalite_apati_kòd(kòd)
    url = _webhook_url(kalite)

    # 1) Rekipere kontni orijinal mesaj la
    repons_li = requests.get(f"{url}/messages/{message_id}", timeout=10)
    repons_li.raise_for_status()
    tèks_orijinal = repons_li.json()["content"]

    # 2) Ranplase sèlman liy "Statut" la, kenbe tout rès tèks la
    tèks_modifye = re.sub(
        r"- Statut : .*",
        "- Statut : ✅ **FINI**",
        tèks_orijinal,
    )

    # 3) Voye tounen tèks KONPLÈ a (modifye)
    repons = requests.patch(
        f"{url}/messages/{message_id}",
        json={"content": tèks_modifye},
        timeout=10,
    )
    repons.raise_for_status()


def voye_notifikasyon_san_kraze(
    kòd: str, type_travay: str, infos: str, delè: str, kolaboratè: str
) -> Optional[str]:
    """
    Vèsyon "sekirize" (Faz 2.4) — si Discord echwe pou nenpòt rezon,
    pa leve erè, jis retounen None. Sistèm nan (Sheets) pa dwe kraze
    akoz Discord — notifikasyon se yon bonus, pa yon depandans kritik.
    """
    try:
        return voye_notifikasyon_nouvo_pwoje(kòd, type_travay, infos, delè, kolaboratè)
    except Exception as e:
        import logging
        logging.warning(f"Notifikasyon Discord echwe: {e}")
        return None


def edite_mesaj_fini_san_kraze(kòd: str, message_id: str) -> bool:
    """
    Vèsyon "sekirize" (Faz 2.4) pou edisyon. Retounen True si reyisi,
    False si echwe (san leve erè).
    """
    try:
        edite_mesaj_fini(kòd, message_id)
        return True
    except Exception:
        return False
