"""
JA-GALI — Faz 3.3 : Jesyon Depans

Modil sa a pèmèt nou verifye kategori depans yo epi anrejistre yo nan
Google Sheets la.
"""

from datetime import date
from typing import List
from sheets_service import ekri_antre_pwoje

# Lis 5 kategori depans yo otorize
KATEGORI_DEPANS = [
    "Payroll",
    "Enpresyon",
    "Abònman",
    "Materyèl",
    "Fonksyonman"
]


def ajoute_depans(
    kategori: str,
    deskripsyon: str,
    montan: float,
    non_depans: str
) -> dict:
    """
    Anrejistre yon depans nan Sheets la apre li fin valide kategori a.
    """
    # Nòmalize kategori a pou asire l matche fòma ki kòrèk la
    kategori_nòmalize = kategori.strip().capitalize()
    
    # Ti ajisteman pou Payroll ki gen lèt majiskil nan kòmansman
    pwòp_kategori = None
    for kat in KATEGORI_DEPANS:
        if kat.upper() == kategori_nòmalize.upper():
            pwòp_kategori = kat
            break

    if pwòp_kategori is None:
        raise ValueError(
            f"Kategori depans '{kategori}' la envalid. "
            f"Kategori otorize yo se: {', '.join(KATEGORI_DEPANS)}"
        )

    dat_jodi_a = date.today().strftime("%d/%m/%Y")
    type_operat = "Depans"

    # Pou depans: Montan sèlman ranpli, Payer ak Kolaboratè rete vid ("")
    liy_nimewo = ekri_antre_pwoje(
        dat=dat_jodi_a,
        type_operat=type_operat,
        kliyan=non_depans,
        categorie=pwòp_kategori,
        description=deskripsyon,
        montan=montan,
        payer="",
        kolaboratè=""
    )

    return {
        "siksè": True,
        "liy": liy_nimewo,
        "kategori": pwòp_kategori,
        "deskripsyon": deskripsyon,
        "montan": montan,
        "non_depans": non_depans,
        "mesaj": f"Depans {montan} anrejistre pou '{non_depans}' nan kategori '{pwòp_kategori}'."
    }

