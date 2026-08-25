"""
JA-GALI — Faz 3.4 & 3.5 : Jesyon Payroll

Modil sa a kalkile lajan chak kolaboratè fè selon kolòn %Kolab ak Kolaboratè
pou yon peryòd ki chwazi (1 mwa, 2 mwa, oswa 3 mwa).
"""

from datetime import datetime, date, timedelta
from typing import Dict, Any
from sheets_service import li_liy

def rezime_payroll(mwa_kont: int = 3) -> dict:
    """
    Li Sheets la, filtre liy yo pa dat, epi gwoupe pa Kolaboratè:
      - Som kolòn %Kolab pou chak Kolaboratè
    Peryòd la detèmine pa 'mwa_kont' (1 mwa, 2 mwa, oswa 3 mwa).
    """
    # Nou li ranje A:Q pou gen Dat (A) ak tout done jiska Kolaboratè (Q)
    liy_yo = li_liy("A:Q")
    if not liy_yo:
        return {"siksè": True, "mwa_kont": mwa_kont, "data": {}, "mesaj": "Pa gen done nan Sheets la."}

    entete = liy_yo[0]
    
    # Jwenn endèks kòlòn yo otomatikman
    idx_dat = 0  # Default A
    idx_kolaboratè = 16  # Default Q
    idx_kolab_pousantaj = -1  # Pou %Kolab

    for i, selil in enumerate(entete):
        selil_clean = selil.strip().upper()
        if "DAT" in selil_clean:
            idx_dat = i
        elif "KOLABORATÈ" in selil_clean or "COLABORATEUR" in selil_clean:
            idx_kolaboratè = i
        elif "%KOLAB" in selil_clean or "% KOLAB" in selil_clean:
            idx_kolab_pousantaj = i

    # Si nou pa jwenn %Kolab, nou gade lòt varyasyon
    if idx_kolab_pousantaj == -1:
        for i, selil in enumerate(entete):
            if "KOLAB" in selil.strip().upper():
                idx_kolab_pousantaj = i
                break
        if idx_kolab_pousantaj == -1:
            idx_kolab_pousantaj = 12  # M pa egzanp

    # Kalkile dat limit la (dènye 1, 2, oswa 3 mwa)
    jodi_a = date.today()
    limit_dat = jodi_a - timedelta(days=30 * mwa_kont)

    payroll_data = {}

    for liy in liy_yo[1:]:
        if not liy or len(liy) <= idx_dat:
            continue

        # 1) Parse dat liy lan
        dat_tèks = liy[idx_dat].strip()
        try:
            dat_obj = datetime.strptime(dat_tèks, "%d/%m/%Y").date()
        except ValueError:
            # Si fòma a diferan, eseye lòt fòma oswa sote liy lan
            try:
                dat_obj = datetime.strptime(dat_tèks, "%Y-%m-%d").date()
            except ValueError:
                continue

        # Filtre pa dat
        if dat_obj < limit_dat:
            continue

        # 2) Rekipere Kolaboratè ak %Kolab
        nom_kolab = liy[idx_kolaboratè].strip() if len(liy) > idx_kolaboratè else ""
        if not nom_kolab or nom_kolab == "-":
            continue

        try:
            pousantaj_val = float(str(liy[idx_kolab_pousantaj]).replace(",", ".").replace(" ", "")) if len(liy) > idx_kolab_pousantaj and liy[idx_kolab_pousantaj] else 0.0
        except ValueError:
            pousantaj_val = 0.0

        if pousantaj_val <= 0:
            continue

        # Nòmalize non kolaboratè a
        non_clean = nom_kolab.strip().capitalize()
        if non_clean not in payroll_data:
            payroll_data[non_clean] = 0.0

        payroll_data[non_clean] += pousantaj_val

    # Nòmalize chif yo (de chif aprè virgil)
    for non_clean in payroll_data:
        payroll_data[non_clean] = round(payroll_data[non_clean], 2)

    return {
        "siksè": True,
        "mwa_kont": mwa_kont,
        "data": payroll_data,
        "mesaj": f"Rapò payroll pou dènye {mwa_kont} mwa a kalkile kòrèkteman."
    }
