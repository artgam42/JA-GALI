"""
JA-GALI — Faz 5.2 : Koneksyon Google Drive

Nouvo apwòch (dapre desizyon final): tout fichye (imaj/videyo) yo
antre nan YON SÈL dosye santral Drive, san okenn konvansyon non. Yo
LYE ak yon piblikasyon atravè yon lyen dirèk kole nan pwopriete
"Fichye" nan Notion (gade notion_service.py).

Kidonk backend lan pa "chèche" nan Drive — li resevwa yon LIS LYEN
Drive (soti Notion), ekstrè ID fichye a nan chak lyen, epi li
metadata/kontni fichye a dirèkteman pa ID.

Kle nesesè nan .env:
    GOOGLE_SERVICE_ACCOUNT_FILE → fichye service-account.json

⚠️ Dosye santral la (ak fichye ladan l) dwe pataje ak email service
   account (gade service-account.json → "client_email") kòm "Viewer".
"""

import os
import re
from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]

# Tip MIME nou konsidere kòm imaj (vrè analiz Claude vizyon)
MIME_IMAJ_AKSEPTE = {
    "image/jpeg",
    "image/png",
    "image/gif",
    "image/webp",
}


class LyenDrivePaValidErreur(Exception):
    """Leve lè yon lyen pa sanble ak yon lyen Google Drive valid."""
    pass


def _sèvis_drive():
    """
    Kreye ak retounen yon kliyan API Google Drive, otantifye ak
    service account (menm fichye JSON ak Sheets/Calendar).
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
    return build("drive", "v3", credentials=kredansyèl)


# ── Ekstraksyon ID Drive nan yon lyen ─────────────────────────────────

_PATÈN_ID_DRIVE = [
    re.compile(r"/d/([a-zA-Z0-9_-]{20,})"),        # .../file/d/ID/view
    re.compile(r"[?&]id=([a-zA-Z0-9_-]{20,})"),    # ...?id=ID oswa &id=ID
]


def ekstrè_id_drive(lyen: str) -> str:
    """
    Ekstrè ID fichye Drive nan yon lyen pataj Google Drive.

    Sipòte fòma: /file/d/ID/view, ?id=ID, /open?id=ID

    Leve LyenDrivePaValidErreur si okenn modèl pa matche.
    """
    for patèn in _PATÈN_ID_DRIVE:
        m = patèn.search(lyen)
        if m:
            return m.group(1)

    raise LyenDrivePaValidErreur(f"Lyen Drive pa rekonèt: '{lyen}'")


# ── Fonksyon piblik ───────────────────────────────────────────────────


def jwenn_metadata_fichye(fichye_id: str) -> dict:
    """
    Jwenn metadata (non, mimeType) yon fichye Drive pa ID.

    Retounen {"id": str, "non": str, "mime_type": str}.
    """
    sèvis = _sèvis_drive()
    rezilta = (
        sèvis.files()
        .get(fileId=fichye_id, fields="id, name, mimeType")
        .execute()
    )
    return {
        "id": rezilta["id"],
        "non": rezilta["name"],
        "mime_type": rezilta["mimeType"],
    }


def telechaje_fichye(fichye_id: str) -> bytes:
    """Telechaje kontni brit (byt) yon fichye Drive pa ID."""
    sèvis = _sèvis_drive()
    return sèvis.files().get_media(fileId=fichye_id).execute()


def jwenn_fichye_pa_lyen(lyen_yo: list) -> list:
    """
    Pran yon lis lyen Drive (soti Notion "Fichye"), retounen metadata
    chak fichye ki valid.

    Retounen yon lis dict: [{"id", "non", "mime_type", "lyen"}, ...]
    Lyen ki pa valid yo senpleman sote (pa kraze tout operasyon an).
    """
    fichye_yo = []

    for lyen in lyen_yo:
        try:
            fichye_id = ekstrè_id_drive(lyen)
            metadata = jwenn_metadata_fichye(fichye_id)
            metadata["lyen"] = lyen
            fichye_yo.append(metadata)
        except (LyenDrivePaValidErreur, Exception):
            continue  # sote lyen ki pa valid oswa fichye ki pa aksesib

    return fichye_yo
