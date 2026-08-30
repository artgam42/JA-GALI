"""
JA-GALI — Faz 6.1 : Koneksyon Google Docs

Fonksyon pou kreye yon nouvo dokiman Google Docs (rapò) nan yon dosye
Drive dedye, epi ekri tèks estriktire ladan l.

Kle nesesè nan .env:
    GOOGLE_DRIVE_DOSYE_RAPÒ_ID → ID dosye Drive kote rapò yo kreye
    GOOGLE_SERVICE_ACCOUNT_FILE → fichye service-account.json (menm youn)

⚠️ Dosye rapò a dwe pataje ak email service account kòm "Editor"
   (pa sèlman "Viewer" — backend lan dwe ka KREYE fichye ladan l).
"""

import os
from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = [
    "https://www.googleapis.com/auth/documents",
    "https://www.googleapis.com/auth/drive",
]


def _kredansyèl():
    fichye_kle = os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE", "service-account.json")

    if not os.path.exists(fichye_kle):
        raise FileNotFoundError(
            f"Fichye service account pa jwenn: '{fichye_kle}'."
        )

    return service_account.Credentials.from_service_account_file(
        fichye_kle, scopes=SCOPES
    )


def _sèvis_docs():
    return build("docs", "v1", credentials=_kredansyèl())


def _sèvis_drive():
    return build("drive", "v3", credentials=_kredansyèl())


def _dosye_rapò_id() -> str:
    dosye_id = os.getenv("GOOGLE_DRIVE_DOSYE_RAPÒ_ID")
    if not dosye_id:
        raise ValueError("GOOGLE_DRIVE_DOSYE_RAPÒ_ID pa konfigire nan .env.")
    return dosye_id


def kreye_rapò(tit: str, tèks_rapò: str) -> dict:
    """
    Kreye yon nouvo Google Doc DIRÈKTEMAN anndan dosye rapò a, ekri
    tèks_rapò ladan l.

    ⚠️ Nou kreye dokiman an atravè Drive API (pa Docs API) epi presize
    'parents' dirèkteman nan kreyasyon an — sa evite yon erè 403 "The
    caller does not have permission" ki rive si w kreye ak Docs API
    san presize dosye, paske service account yo pa gen pwòp kota
    depo Google ankò (yo dwe kreye fichye DIRÈKTEMAN nan yon dosye ki
    gen yon pwopriyetè ak kota, tankou dosye rapò ou a).

    Retounen: {"id": str, "lyen": str} (lyen pou louvri dokiman an).
    """
    sèvis_docs = _sèvis_docs()
    sèvis_drive = _sèvis_drive()
    dosye_id = _dosye_rapò_id()

    # 1) Kreye dokiman Google Docs la DIRÈKTEMAN anndan dosye a
    metadata = {
        "name": tit,
        "mimeType": "application/vnd.google-apps.document",
        "parents": [dosye_id],
    }
    fichye = sèvis_drive.files().create(body=metadata, fields="id").execute()
    dòk_id = fichye["id"]

    # 2) Ekri tèks rapò a nan kò dokiman an
    sèvis_docs.documents().batchUpdate(
        documentId=dòk_id,
        body={
            "requests": [
                {
                    "insertText": {
                        "location": {"index": 1},
                        "text": tèks_rapò,
                    }
                }
            ]
        },
    ).execute()

    lyen = f"https://docs.google.com/document/d/{dòk_id}/edit"
    return {"id": dòk_id, "lyen": lyen}
