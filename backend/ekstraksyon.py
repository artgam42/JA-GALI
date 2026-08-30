"""
JA-GALI — Faz 1.5 : Ekstraksyon done ak Claude

Li yon mesaj an lang natirèl, ekstrè enfo pwojè yo (kliyan, tip
travay, infos, delè, kolaboratè, montan, peye) atravè Claude API.

Si enfo KRITIK yo (kliyan, tip_travay, montan) manke oswa pa klè,
Claude retounen yon kesyon pou poze itilizatè a, olye kreye done
enkonplè.
"""

import os
import json


PROMPT_SISTÈM = """Ou se yon asistan ki ekstrè enfo pwojè travay pou yon ajans kominikasyon vizyèl (JUST ART), apati yon mesaj lib an Kreyòl ayisyen.

Ekstrè chan sa yo nan mesaj la:
- kliyan: non kliyan an (OBLIGATWA)
- tip_travay: tip travay la (egzanp "Flyer", "Logo", "Videyo") (OBLIGATWA)
- infos: kout deskripsyon adisyonèl sou travay la (si pa gen plis detay pase tip_travay, itilize menm valè ak tip_travay)
- delè: dat/moman pou remèt travay la, jan itilizatè a ekri l (si pa mansyone, ekri "Pa presize")
- kolaboratè: non moun k ap reyalize travay la (si pa mansyone, kite vid "")
- montan: pri total travay la, an chif sèlman san senbòl (OBLIGATWA — si pa gen okenn pri mansyone, sa a manke)
- peye: kantite lajan kliyan an DEJA peye kounye a, an chif (si pa mansyone, itilize 0)

Si youn nan chan OBLIGATWA yo (kliyan, tip_travay, montan) pa klè oswa pa prezan nan mesaj la, REPONN SÈLMAN ak JSON sa a (ranplase kesyon an ak yon kesyon kout, zanmitay, an Kreyòl, ki mande SÈLMAN enfo ki manke yo):
{"pare": false, "kesyon": "..."}

Si tout chan OBLIGATWA yo klè, REPONN SÈLMAN ak JSON sa a (ranplase valè yo):
{"pare": true, "kliyan": "...", "tip_travay": "...", "infos": "...", "delè": "...", "kolaboratè": "...", "montan": 0, "peye": 0}

Règ estrikt: PA janm ekri okenn tèks anplis, okenn eksplikasyon, okenn backtick markdown. Repons ou an dwe kòmanse dirèkteman ak { epi fini ak }."""


class EkstraksyonErreur(Exception):
    """Leve lè Claude retounen yon repons nou pa ka analize kòm JSON valid."""
    pass


def ekstrè_pwoje(mesaj: str) -> dict:
    """
    Rele Claude API pou ekstrè enfo pwojè nan yon mesaj lib.

    Retounen yon dict — swa:
        {"pare": False, "kesyon": str}
    swa:
        {"pare": True, "kliyan": str, "tip_travay": str, "infos": str,
         "delè": str, "kolaboratè": str, "montan": float, "peye": float}

    Leve EkstraksyonErreur si repons Claude a pa JSON valid.
    """
    from anthropic import Anthropic

    kle = os.getenv("ANTHROPIC_API_KEY")
    modèl = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-6")
    client = Anthropic(api_key=kle)

    repons = client.messages.create(
        model=modèl,
        max_tokens=500,
        system=PROMPT_SISTÈM,
        messages=[{"role": "user", "content": mesaj}],
    )

    tèks = repons.content[0].text.strip()

    # Pwoteksyon si Claude mete backticks markdown malgre enstriksyon an
    if tèks.startswith("```"):
        tèks = tèks.strip("`")
        if tèks.lower().startswith("json"):
            tèks = tèks[4:]
        tèks = tèks.strip()

    try:
        done = json.loads(tèks)
    except json.JSONDecodeError as e:
        raise EkstraksyonErreur(
            f"Claude pa retounen JSON valid: {tèks[:200]}"
        ) from e

    if done.get("pare") is False:
        return {
            "pare": False,
            "kesyon": done.get("kesyon", "Mwen bezwen plis enfo sou pwojè sa a."),
        }

    return {
        "pare": True,
        "kliyan": str(done.get("kliyan", "")).strip(),
        "tip_travay": str(done.get("tip_travay", "")).strip(),
        "infos": str(done.get("infos", "")).strip() or str(done.get("tip_travay", "")).strip(),
        "delè": str(done.get("delè", "Pa presize")).strip(),
        "kolaboratè": str(done.get("kolaboratè", "")).strip(),
        "montan": float(done.get("montan", 0) or 0),
        "peye": float(done.get("peye", 0) or 0),
    }
