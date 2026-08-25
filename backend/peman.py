"""
JA-GALI — Faz 3.2 : Jesyon Peman Kliyan

Modil sa a kalkile rès dwe sou yon pwojè epi ajoute nouvo liy tranzaksyon
lè yon kliyan peye yon rès kòb (Solde).
"""

from datetime import date
from typing import Optional, Tuple, Dict, Any
from sheets_service import jwenn_liy_pa_kòd, ekri_antre_pwoje, li_liy


def kalkile_rès_dwe(kòd_pwoje: str) -> Tuple[float, Dict[str, Any]]:
    """
    Kalkile rès lajan yon kliyan dwe sou yon pwojè, epi rekipere enfo orijinal yo.

    Formil:
        original_montan = Montan ki nan premye antre pwojè a (san ": Solde")
        total_payer = Som tout "Payer" ki fèt sou kòd sa a
        rès_dwe = original_montan - total_payer

    Retounen:
        Tuple (rès_dwe, enfo_orijinal)
        kote enfo_orijinal gen ladan: kliyan, kolaboratè, kategori.
    """
    liy_yo = jwenn_liy_pa_kòd(kòd_pwoje)
    if not liy_yo:
        raise ValueError(f"Pa gen okenn pwojè ki jwenn ak kòd '{kòd_pwoje}' nan Sheets la.")

    # Rekipere premye liy (entete) nan Sheets la pou nou jwenn bon endèks yo
    entete_liy = li_liy("A:Q")
    idx_kliyan = 2          # Default C
    idx_kolaboratè = 16     # Default Q

    if entete_liy:
        entete = entete_liy[0]
        for i, selil in enumerate(entete):
            selil_clean = selil.strip().upper()
            if "KLIYAN" in selil_clean or "FOURNIS" in selil_clean:
                idx_kliyan = i
            elif "KOLABORATÈ" in selil_clean or "COLABORATEUR" in selil_clean:
                idx_kolaboratè = i

    original_montan = 0.0
    total_payer = 0.0
    enfo_orijinal = {
        "kliyan": "",
        "kolaboratè": "",
        "categorie": "Revni Sèvis"
    }

    kòd_nòmalize = kòd_pwoje.strip().upper()

    for liy in liy_yo:
        # Deskripsyon (Index 4)
        desc = liy[4].strip() if len(liy) > 4 else ""
        is_solde = ": SOLDE" in desc.upper()

        # Konvèti Montan (Index 5) ak Payer (Index 6) an float
        try:
            m = float(str(liy[5]).replace(",", ".").replace(" ", "")) if len(liy) > 5 and liy[5] else 0.0
        except ValueError:
            m = 0.0

        try:
            p = float(str(liy[6]).replace(",", ".").replace(" ", "")) if len(liy) > 6 and liy[6] else 0.0
        except ValueError:
            p = 0.0

        total_payer += p

        # Si se premye liy lan (orijinal la, ki pa gen ": Solde")
        if not is_solde and original_montan == 0.0:
            original_montan = m
            enfo_orijinal["kliyan"] = liy[idx_kliyan] if len(liy) > idx_kliyan else ""
            enfo_orijinal["kolaboratè"] = liy[idx_kolaboratè] if len(liy) > idx_kolaboratè else ""

    # Si nou pa t jwenn premye liy lan pou nenpòt rezon (men gen lòt liy),
    # pran enfòmasyon nan premye liy ki disponib la
    if not enfo_orijinal["kliyan"] and liy_yo:
        enfo_orijinal["kliyan"] = liy_yo[0][idx_kliyan] if len(liy_yo[0]) > idx_kliyan else ""
        enfo_orijinal["kolaboratè"] = liy_yo[0][idx_kolaboratè] if len(liy_yo[0]) > idx_kolaboratè else ""

    rès_dwe = max(0.0, original_montan - total_payer)
    return rès_dwe, enfo_orijinal



def ajoute_peman(kòd_pwoje: str, montan_payer: float) -> dict:
    """
    Anrejistre yon nouvo peman pou yon pwojè ki te dwe.
    Kalkile rès la otomatikman epi mete l kòm 'Montan' nan nouvo liy lan.
    """
    kòd_nòmalize = kòd_pwoje.strip().upper()
    rès_dwe, enfo = kalkile_rès_dwe(kòd_nòmalize)

    if rès_dwe <= 0:
        return {
            "siksè": False,
            "mesaj": f"Pwojè {kòd_nòmalize} a deja peye konplè (rès dwe = 0)."
        }

    # Nouvo liy peman
    dat_jodi_a = date.today().strftime("%d/%m/%Y")
    type_operat = "Revni"
    categorie = "Revni Sèvis"
    description = f"{kòd_nòmalize} : Solde"
    
    # Valè n ap ekri nan Sheets yo:
    # Montan = rès ki te dwe anvan peman sa a
    # Payer = montan yo bay kounye a
    liy_nimewo = ekri_antre_pwoje(
        dat=dat_jodi_a,
        type_operat=type_operat,
        kliyan=enfo["kliyan"],
        categorie=categorie,
        description=description,
        montan=rès_dwe,
        payer=montan_payer,
        kolaboratè=enfo["kolaboratè"]
    )

    balans_nouvo = max(0.0, rès_dwe - montan_payer)

    return {
        "siksè": True,
        "liy": liy_nimewo,
        "kliyan": enfo["kliyan"],
        "rès_anvan": rès_dwe,
        "peye_kounye_a": montan_payer,
        "nouvo_balans": balans_nouvo,
        "mesaj": f"Peman {montan_payer} anrejistre pou pwojè {kòd_nòmalize}. Nouvo balans: {balans_nouvo}."
    }
