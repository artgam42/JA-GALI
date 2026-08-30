"""
JA-GALI — Faz 4.1/4.2 : Koneksyon Google Calendar

Fonksyon pou kreye evènman sou Google Calendar, konekte ak delè pwojè
yo. Itilize menm service-account.json ak Sheets, men ak yon nouvo
"scope" (calendar) — Calendar la dwe pataje ak email service account
la separeman (gade Faz 4.1 nan fèy wout la).
"""

import os
from datetime import date, datetime, timedelta
from typing import Optional
from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/calendar"]


def _sèvis_calendar():
    """Kreye ak retounen yon kliyan API Google Calendar."""
    fichye_kle = os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE", "service-account.json")
    json_env = os.getenv("GOOGLE_CREDENTIALS_JSON")

    if json_env:
        import json
        try:
            info = json.loads(json_env)
            kredansyèl = service_account.Credentials.from_service_account_info(info, scopes=SCOPES)
        except Exception as e:
            raise ValueError(f"Erè nan GOOGLE_CREDENTIALS_JSON: {e}")
    elif os.path.exists(fichye_kle):
        kredansyèl = service_account.Credentials.from_service_account_file(
            fichye_kle, scopes=SCOPES
        )
    else:
        raise FileNotFoundError(
            f"Fichye service account pa jwenn: '{fichye_kle}' epi GOOGLE_CREDENTIALS_JSON pa konfigire."
        )
    return build("calendar", "v3", credentials=kredansyèl)


def _kalandriye_id() -> str:
    """Li ID Calendar la nan .env."""
    kal_id = os.getenv("GOOGLE_CALENDAR_ID")
    if not kal_id:
        raise ValueError("GOOGLE_CALENDAR_ID pa konfigire nan .env.")
    return kal_id


def kreye_evènman(
    tit: str,
    dat_evènman: date,
    deskripsyon: str = "",
) -> str:
    """
    Kreye yon evènman "tout jounen" (all-day) sou Calendar la.

    Retounen: ID evènman Google Calendar la.
    """
    sèvis = _sèvis_calendar()
    kal_id = _kalandriye_id()

    dat_fen = dat_evènman + timedelta(days=1)  # Google Calendar mande "end" eksklizif

    evènman = {
        "summary": tit,
        "description": deskripsyon,
        "start": {"date": dat_evènman.isoformat()},
        "end": {"date": dat_fen.isoformat()},
    }

    rezilta = (
        sèvis.events()
        .insert(calendarId=kal_id, body=evènman)
        .execute()
    )
    return rezilta["id"]


def ajoute_delè_pwoje(kòd_pwoje: str, dat_delè: date) -> str:
    """
    Kreye yon evènman Calendar pou delè yon pwojè (Faz 4.2).

    Retounen: ID evènman an.
    """
    tit = f"⏰ Delè: {kòd_pwoje.upper()}"
    deskripsyon = f"Delè pou remèt travay pwojè {kòd_pwoje.upper()}."
    return kreye_evènman(tit, dat_delè, deskripsyon)


# ── Faz 4.4 — Li evènman k ap pwoche (pou paj "Alèt" PWA) ────────────


def lis_evènman_k_ap_pwoche(jou_alavans: int = 30) -> list:
    """
    Jwenn tout evènman ki soti jodi a jiska X jou nan avni, triye pa
    dat pwochèn.

    Retounen yon lis dict: [{"tit": str, "dat": "AAAA-MM-JJ"}, ...]
    """
    sèvis = _sèvis_calendar()
    kal_id = _kalandriye_id()

    jodi = datetime.utcnow()
    limit = jodi + timedelta(days=jou_alavans)

    rezilta = (
        sèvis.events()
        .list(
            calendarId=kal_id,
            timeMin=jodi.isoformat() + "Z",
            timeMax=limit.isoformat() + "Z",
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )

    evènman_yo = []
    for ev in rezilta.get("items", []):
        dat_brit = ev["start"].get("date") or ev["start"].get("dateTime", "")[:10]
        evènman_yo.append({
            "tit": ev.get("summary", "(San tit)"),
            "dat": dat_brit,
        })

    return evènman_yo
