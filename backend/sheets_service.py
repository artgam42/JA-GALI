"""
JA-GALI — Faz 1.3 : Koneksyon Google Sheets

Fonksyon pou li ak ekri sou Sheet "Journal JUST ART" (onglè "Journal Unique 26").

⚠️ RÈG KRITIK (gade Contexte.md §6):
Backend lan ekri SÈLMAN nan kòlòn "done bri" yo. Kòlòn fòmil otomatik yo
(Solde, Balans Kès, Net/A.Enpr, %JUSTART, %Kolab, Antre Kès, Sòti Kès)
PA JANM touche — Sheets la kalkile yo pou kont li.

Mapping kòlòn (gade Contexte.md §6 pou detay konplè):
    A = Dat            B = Type Opérat.    C = Kliyan/Fournis.
    D = Catégorie       E = Description     F = Montan
    G = Payer           Q = Kolaboratè
(H, I, J, K, L, N, O, P, R, S = fòmil otomatik, PA touche)
"""

import os
from typing import Optional
from google.oauth2 import service_account
from googleapiclient.discovery import build

# ── Konfigirasyon ─────────────────────────────────────────────────────

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# Kòlòn kote nou ekri "done bri" yo (gade nòt anwo a — pa kontigu)
KÒLÒN_PRENSIPAL = "A:G"   # Dat, Type Opérat., Kliyan, Catégorie, Description, Montan, Payer
KÒLÒN_KOLABORATÈ = "Q"    # Kolaboratè (izole, apre kòlòn fòmil yo)


def _sèvis_sheets():
    """
    Kreye ak retounen yon kliyan API Google Sheets, otantifye ak
    service account (fichye JSON nan GOOGLE_SERVICE_ACCOUNT_FILE).
    """
    fichye_kle = os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE", "service-account.json")

    if not os.path.exists(fichye_kle):
        raise FileNotFoundError(
            f"Fichye service account pa jwenn: '{fichye_kle}'. "
            f"Verifye li nan dosye backend/ epi non li matche "
            f"GOOGLE_SERVICE_ACCOUNT_FILE nan .env."
        )

    kredansyèl = service_account.Credentials.from_service_account_file(
        fichye_kle, scopes=SCOPES
    )
    return build("sheets", "v4", credentials=kredansyèl)


def _id_sheet_ak_onglè():
    """Li ID Sheet la ak non onglè a nan .env, epi valide yo prezan."""
    sheet_id = os.getenv("GOOGLE_SHEET_ID")
    onglè = os.getenv("GOOGLE_SHEET_ONGLE", "Journal Unique 26")

    if not sheet_id:
        raise ValueError("GOOGLE_SHEET_ID pa konfigire nan .env.")

    return sheet_id, onglè


# ── Fonksyon piblik ───────────────────────────────────────────────────


def li_liy(range_a: str = "A:G"):
    """
    Li valè nan yon ranje kolòn (egzanp "A:G") sou onglè prensipal la.
    Retounen yon lis lis (chak sou-lis se yon liy).
    """
    sèvis = _sèvis_sheets()
    sheet_id, onglè = _id_sheet_ak_onglè()

    rezilta = (
        sèvis.spreadsheets()
        .values()
        .get(spreadsheetId=sheet_id, range=f"'{onglè}'!{range_a}")
        .execute()
    )
    return rezilta.get("values", [])


def li_valè_brit(range_a: str):
    """
    Menm jan ak li_liy(), men mande valè "brit" (chif reyèl, pa tèks
    fòmate tankou '$1,200.00') — nesesè pou kalkil (sonm montan, elt.).
    Itilize pa rapo_service.py (Faz 6) pou kalkile total revni/depans.
    """
    sèvis = _sèvis_sheets()
    sheet_id, onglè = _id_sheet_ak_onglè()

    rezilta = (
        sèvis.spreadsheets()
        .values()
        .get(
            spreadsheetId=sheet_id,
            range=f"'{onglè}'!{range_a}",
            valueRenderOption="UNFORMATTED_VALUE",
        )
        .execute()
    )
    return rezilta.get("values", [])


def jwenn_pwochen_liy_vid() -> int:
    """
    Detèmine premye liy vid disponib nan onglè a, ann analize kòlòn A
    (Dat) — kòlòn ki toujou gen valè pou chak vrè liy done.

    Retounen nimewo liy la (1-indexed, jan Google Sheets fè l).
    """
    valè = li_liy("A:A")
    # valè[0] se antèt la ("Dat") — done reyèl yo kòmanse liy 2.
    # Nou chèche premye liy ki vid apre dènye liy ki gen done.
    return len(valè) + 1


def ekri_antre_pwoje(
    dat: str,
    type_operat: str,
    kliyan: str,
    categorie: str,
    description: str,
    montan,
    payer,
    kolaboratè: str,
) -> int:
    """
    Ajoute yon nouvo liy nan Journal la ak done "bri" yo sèlman.

    Paramèt yo koresponn dirèkteman ak kòlòn A-G + Q. AUKENN lòt kòlòn
    (Solde, Balans Kès, elatriye) pa touche — Sheets la kalkile yo.

    Retounen: nimewo liy ki fèk kreye a (pou lòt fonksyon ka referans li).
    """
    sèvis = _sèvis_sheets()
    sheet_id, onglè = _id_sheet_ak_onglè()

    liy = jwenn_pwochen_liy_vid()

    # 1) Ekri kòlòn A jiska G (kontigu)
    valè_prensipal = [[dat, type_operat, kliyan, categorie, description, montan, payer]]
    sèvis.spreadsheets().values().update(
        spreadsheetId=sheet_id,
        range=f"'{onglè}'!A{liy}:G{liy}",
        valueInputOption="USER_ENTERED",
        body={"values": valè_prensipal},
    ).execute()

    # 2) Ekri kòlòn Q (Kolaboratè) apa, paske li pa kontigu ak A:G
    sèvis.spreadsheets().values().update(
        spreadsheetId=sheet_id,
        range=f"'{onglè}'!{KÒLÒN_KOLABORATÈ}{liy}",
        valueInputOption="USER_ENTERED",
        body={"values": [[kolaboratè]]},
    ).execute()

    return liy


def jwenn_liy_pa_kòd(kòd_pwoje: str) -> list[list]:
    """
    Chèche tout liy nan Journal la ki lye ak yon kòd pwojè.
    Li kolòn A:Q (pou gen done prensipal yo ak kolaboratè a).

    Retounen yon lis lis, kote chak lis reprezante yon liy ki koresponn.
    """
    kòd_nòmalize = kòd_pwoje.strip().upper()
    liy_yo = li_liy("A:Q")

    liy_filtre = []
    for liy in liy_yo:
        # Deskripsyon an nan kolòn E (endèks 4)
        if len(liy) > 4:
            deskripsyon = liy[4].strip()
            # Tcheke si deskripsyon an kòmanse ak kòd pwojè a
            if deskripsyon.upper().startswith(kòd_nòmalize):
                rès = deskripsyon[len(kòd_nòmalize):].strip()
                if not rès or rès.startswith(":") or rès.startswith("-"):
                    liy_filtre.append(liy)

    return liy_filtre


# ── Faz 1.7 / Faz 2 — Onglè kache pou message_id Discord ────────────

#
# Onglè "Discord_IDs" (kache, pa vizib nan itilizasyon nòmal Sheet la)
# kenbe mapping: Kòd Pwojè | Message ID — pou nou ka edite mesaj
# Discord orijinal la lè yon pwojè make FINI (gade Contexte.md).

ONGLÈ_DISCORD_IDS = "Discord_IDs"


def estoke_message_id(kòd_pwoje: str, message_id: str) -> None:
    """
    Anrejistre yon nouvo koup (Kòd Pwojè, Message ID) nan onglè
    Discord_IDs. Apele sa apre 2.3 (premye mesaj Discord voye a).
    """
    sèvis = _sèvis_sheets()
    sheet_id, _ = _id_sheet_ak_onglè()

    # Jwenn pwochen liy vid nan onglè Discord_IDs (kolòn A)
    rezilta = (
        sèvis.spreadsheets()
        .values()
        .get(spreadsheetId=sheet_id, range=f"'{ONGLÈ_DISCORD_IDS}'!A:A")
        .execute()
    )
    liy = len(rezilta.get("values", [])) + 1

    sèvis.spreadsheets().values().update(
        spreadsheetId=sheet_id,
        range=f"'{ONGLÈ_DISCORD_IDS}'!A{liy}:B{liy}",
        valueInputOption="USER_ENTERED",
        body={"values": [[kòd_pwoje, message_id]]},
    ).execute()


def jwenn_message_id(kòd_pwoje: str) -> Optional[str]:
    """
    Chèche message_id Discord ki lye ak yon kòd pwojè, nan onglè
    Discord_IDs. Retounen None si pa jwenn (pa gen mesaj lye ak kòd la).
    """
    sèvis = _sèvis_sheets()
    sheet_id, _ = _id_sheet_ak_onglè()

    rezilta = (
        sèvis.spreadsheets()
        .values()
        .get(spreadsheetId=sheet_id, range=f"'{ONGLÈ_DISCORD_IDS}'!A:B")
        .execute()
    )
    liy_yo = rezilta.get("values", [])

    kòd_nòmalize = kòd_pwoje.strip().upper()
    for liy in liy_yo:
        if len(liy) >= 2 and liy[0].strip().upper() == kòd_nòmalize:
            return liy[1]

    return None
