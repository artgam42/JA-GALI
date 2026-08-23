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
