"""
JA-GALI — Faz 5.1 : Koneksyon Notion API

Fonksyon pou li enfòmasyon piblikasyon yo (Non + Kontèks) soti nan
database Notion JUST ART.

Estrikti database Notion an:
    - "Non"     → tit/non piblikasyon an (propriete Title)
    - "Kontèks" → brief/kontèks piblikasyon an (propriete Rich Text)

Kle nesesè nan .env:
    NOTION_TOKEN        → kle entegrasyon Notion an
    NOTION_DATABASE_ID  → ID database Notion an
"""

import os
from typing import Optional

import requests

# ── Konfigirasyon ─────────────────────────────────────────────────────

NOTION_API_VERSION = "2022-06-28"
NOTION_BASE_URL = "https://api.notion.com/v1"


def _antèt_notion() -> dict:
    """
    Konstwi antèt HTTP pou rele Notion API.
    Leve ValueError si token an pa konfigire.
    """
    token = os.getenv("NOTION_TOKEN")
    if not token:
        raise ValueError("NOTION_TOKEN pa konfigire nan .env.")
    return {
        "Authorization": f"Bearer {token}",
        "Notion-Version": NOTION_API_VERSION,
        "Content-Type": "application/json",
    }


def _database_id() -> str:
    """Li ID database Notion an nan .env."""
    db_id = os.getenv("NOTION_DATABASE_ID")
    if not db_id:
        raise ValueError("NOTION_DATABASE_ID pa konfigire nan .env.")
    return db_id


# ── Fonksyon piblik ───────────────────────────────────────────────────


def jwenn_piblikasyon_pa_non(non_piblikasyon: str) -> Optional[dict]:
    """
    Chèche yon piblikasyon nan database Notion an pa non egzak li.

    Filtè: propriete "Non" (Title) egal ak non_piblikasyon an.

    Retounen yon dict: {"non": str, "kontèks": str, "fichye": list[str]}
    (fichye = lis lyen URL Drive ki nan pwopriete "Fichye" a)
    Retounen None si pa jwenn okenn rezilta ki koresponn.
    """
    antèt = _antèt_notion()
    db_id = _database_id()

    kò_demann = {
        "filter": {
            "property": "Non",
            "title": {
                "equals": non_piblikasyon.strip()
            }
        }
    }

    repons = requests.post(
        f"{NOTION_BASE_URL}/databases/{db_id}/query",
        headers=antèt,
        json=kò_demann,
        timeout=15,
    )

    if repons.status_code == 404:
        raise ValueError(
            f"Database Notion pa jwenn (ID: {db_id}). "
            f"Verifye NOTION_DATABASE_ID nan .env ak pèmisyon entegrasyon an."
        )

    repons.raise_for_status()
    done = repons.json()

    rezilta_yo = done.get("results", [])
    if not rezilta_yo:
        return None  # Pa jwenn piblikasyon ki gen non sa a

    # Pran premye rezilta ki koresponn
    paj = rezilta_yo[0]
    propriete_yo = paj.get("properties", {})

    non_tèks = _ekstrè_tit(propriete_yo.get("Non", {}))
    kontèks_tèks = _ekstrè_rich_text(propriete_yo.get("Kontèks", {}))
    lyen_fichye = _ekstrè_lyen_fichye(propriete_yo.get("Fichye", {}))

    return {
        "non": non_tèks,
        "kontèks": kontèks_tèks,
        "fichye": lyen_fichye,
    }


def mete_ajou_caption(non_piblikasyon: str, caption: str) -> bool:
    """
    Mete ajou kolòn "Caption" nan liy piblikasyon an (pa non), apre
    itilizatè a klike "Aksepte" nan PWA a.

    Retounen True si mizajou a reyisi.
    Leve ValueError si piblikasyon an pa jwenn nan database la.
    """
    antèt = _antèt_notion()
    db_id = _database_id()

    # 1) Jwenn ID paj la (pa non piblikasyon an)
    kò_demann = {
        "filter": {
            "property": "Non",
            "title": {"equals": non_piblikasyon.strip()},
        }
    }

    repons_rechèch = requests.post(
        f"{NOTION_BASE_URL}/databases/{db_id}/query",
        headers=antèt,
        json=kò_demann,
        timeout=15,
    )
    repons_rechèch.raise_for_status()
    rezilta_yo = repons_rechèch.json().get("results", [])

    if not rezilta_yo:
        raise ValueError(
            f"Pa jwenn piblikasyon '{non_piblikasyon}' nan Notion pou mete ajou caption la."
        )

    paj_id = rezilta_yo[0]["id"]

    # 2) Mete ajou pwopriete "Caption" nan paj la
    kò_mizajou = {
        "properties": {
            "Caption": {
                "rich_text": [
                    {"type": "text", "text": {"content": caption[:2000]}}  # limit Notion
                ]
            }
        }
    }

    repons_mizajou = requests.patch(
        f"{NOTION_BASE_URL}/pages/{paj_id}",
        headers=antèt,
        json=kò_mizajou,
        timeout=15,
    )
    repons_mizajou.raise_for_status()

    return True


def lis_tout_piblikasyon() -> list:
    """
    Retounen lis tout piblikasyon nan database Notion an.
    Itil pou tès ak debogaj.

    Retounen yon lis dict: [{"non": str, "kontèks": str}, ...]
    """
    antèt = _antèt_notion()
    db_id = _database_id()

    repons = requests.post(
        f"{NOTION_BASE_URL}/databases/{db_id}/query",
        headers=antèt,
        json={},
        timeout=15,
    )
    repons.raise_for_status()
    done = repons.json()

    piblikasyon_yo = []
    for paj in done.get("results", []):
        propriete_yo = paj.get("properties", {})
        piblikasyon_yo.append({
            "non": _ekstrè_tit(propriete_yo.get("Non", {})),
            "kontèks": _ekstrè_rich_text(propriete_yo.get("Kontèks", {})),
        })

    return piblikasyon_yo


# ── Fonksyon entèn (ekstraksyon done Notion) ──────────────────────────


def _ekstrè_tit(propriete: dict) -> str:
    """
    Ekstrè tèks plen nan yon propriete Notion de tip "title".
    Retounen '' si vid oswa mal fòmate.
    """
    fragman_yo = propriete.get("title", [])
    return "".join(f.get("plain_text", "") for f in fragman_yo).strip()


def _ekstrè_rich_text(propriete: dict) -> str:
    """
    Ekstrè tèks plen nan yon propriete Notion de tip "rich_text".
    Retounen '' si vid oswa mal fòmate.
    """
    fragman_yo = propriete.get("rich_text", [])
    return "".join(f.get("plain_text", "") for f in fragman_yo).strip()


def _ekstrè_lyen_fichye(propriete: dict) -> list:
    """
    Ekstrè lis lyen URL nan yon propriete Notion de tip "files".

    Jere tou de ka: fichye "external" (lyen ou kole manyèlman, egzanp
    Drive) ak fichye "file" (telechaje dirèkteman nan Notion).

    Retounen yon lis tèks (URL yo). Lis vid si pa gen fichye.
    """
    fichye_yo = propriete.get("files", [])
    lyen_yo = []

    for f in fichye_yo:
        tip = f.get("type")
        if tip == "external":
            url = f.get("external", {}).get("url", "")
        elif tip == "file":
            url = f.get("file", {}).get("url", "")
        else:
            url = ""

        if url:
            lyen_yo.append(url)

    return lyen_yo
