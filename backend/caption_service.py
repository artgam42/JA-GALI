"""
JA-GALI — Faz 5.3 : Jenerasyon Caption ak Claude

Konbine Kontèks Notion + fichye (imaj/videyo) ki lye ak yon
piblikasyon (atravè pwopriete "Fichye" nan Notion), mande Claude
ekri yon caption apwopriye pou rezo sosyal (an Kreyòl).

Imaj yo: Claude VRÈMAN gade yo (vizyon multimodal).
Videyo yo: Claude sèlman wè NON fichye a kòm kontèks tèks (pa gen
vrè analiz videyo — Claude pa "gade" kontni videyo dirèkteman).

⚠️ BEZWEN KREDI API CLAUDE pou fonksyone reyèlman — menm depandans ak
Faz 1.5. Kòd la konplè epi teste (sentaks + lojik san apèl reyèl).
"""

import os
import base64


class PiblikasyonPaJwennErreur(Exception):
    """Leve lè Notion pa gen okenn antre pou non_piblikasyon an."""
    pass


def genere_caption(non_piblikasyon: str, max_imaj: int = 3) -> dict:
    """
    Woutin konplè Faz 5.3:
        1. Jwenn Kontèks + lyen Fichye nan Notion
        2. Ekstrè ID/metadata chak fichye Drive (imaj + videyo)
        3. Voye kontèks + imaj (vrè vizyon) + non videyo yo bay Claude
        4. Retounen caption Claude jenere a

    Retounen: {"non", "kontèks", "kantite_imaj", "kantite_videyo", "caption"}
    Leve PiblikasyonPaJwennErreur si Notion pa gen okenn antre pou
    non_piblikasyon an.
    """
    from notion_service import jwenn_piblikasyon_pa_non
    from drive_service import jwenn_fichye_pa_lyen, MIME_IMAJ_AKSEPTE

    enfo_notion = jwenn_piblikasyon_pa_non(non_piblikasyon)
    if enfo_notion is None:
        raise PiblikasyonPaJwennErreur(
            f"Pa jwenn piblikasyon '{non_piblikasyon}' nan database Notion an."
        )

    lyen_yo = enfo_notion.get("fichye", [])
    fichye_yo = jwenn_fichye_pa_lyen(lyen_yo)

    imaj_yo = [f for f in fichye_yo if f["mime_type"] in MIME_IMAJ_AKSEPTE]
    videyo_yo = [f for f in fichye_yo if f["mime_type"].startswith("video/")]

    caption = _jenere_ak_claude(
        non=non_piblikasyon,
        kontèks=enfo_notion.get("kontèks", ""),
        imaj_yo=imaj_yo[:max_imaj],
        videyo_yo=videyo_yo,
    )

    return {
        "non": non_piblikasyon,
        "kontèks": enfo_notion.get("kontèks", ""),
        "kantite_imaj": len(imaj_yo),
        "kantite_videyo": len(videyo_yo),
        "caption": caption,
    }


def _jenere_ak_claude(non: str, kontèks: str, imaj_yo: list, videyo_yo: list) -> str:
    """
    Apèl Claude API (vizyon multimodal pou imaj, tèks sèlman pou videyo).
    """
    from anthropic import Anthropic
    from drive_service import telechaje_fichye

    kle = os.getenv("ANTHROPIC_API_KEY")
    modèl = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-6")
    client = Anthropic(api_key=kle)

    tèks_videyo = ""
    if videyo_yo:
        non_videyo_yo = ", ".join(v["non"] for v in videyo_yo)
        tèks_videyo = f"\n\nGen tou {len(videyo_yo)} videyo mare ak pòs sa a: {non_videyo_yo}."

    kontni_mesaj = [
        {
            "type": "text",
            "text": (
                f"Ou se yon espesyalis kominikasyon rezo sosyal pou ajans "
                f"JUST ART. Ekri yon caption an Kreyòl ayisyen, kout (2-4 fraz), "
                f"angajan, ak 2-3 hashtag apwopriye, pou piblikasyon '{non}'.\n\n"
                f"Kontèks/brief: {kontèks or '(pa gen kontèks bay)'}"
                f"{tèks_videyo}\n\n"
                f"Gade imaj yo ki mare ak pòs la pou enspirasyon si genyen."
            ),
        }
    ]

    for imaj in imaj_yo:
        try:
            byt_imaj = telechaje_fichye(imaj["id"])
            b64 = base64.b64encode(byt_imaj).decode("utf-8")
            kontni_mesaj.append({
                "type": "image",
                "source": {"type": "base64", "media_type": imaj["mime_type"], "data": b64},
            })
        except Exception:
            continue  # si yon imaj echwe telechaje, kontinye san l

    repons = client.messages.create(
        model=modèl,
        max_tokens=300,
        messages=[{"role": "user", "content": kontni_mesaj}],
    )

    return repons.content[0].text
