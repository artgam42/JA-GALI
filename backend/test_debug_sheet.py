"""
Dyagnostik — Wè done brit Sheets pou konprann poukisa payroll vid.

Itilizasyon:
    python3 test_debug_sheet.py
"""

import os
from dotenv import load_dotenv

load_dotenv()

from sheets_service import li_valè_brit
from dat_util import pars_dat
from datetime import date, timedelta


def teste():
    liy_yo = li_valè_brit("A:R")

    if not liy_yo:
        print("❌ Pa gen okenn done nan Sheets la ditou.")
        return

    entete = [str(c) for c in liy_yo[0]]
    print("📋 ANTÈT KÒLÒN YO (A jiska R):")
    for i, non in enumerate(entete):
        lèt_kòlòn = chr(ord("A") + i)
        print(f"   {lèt_kòlòn} (endèks {i}): '{non}'")

    print(f"\n📊 Kantite liy total (san antèt): {len(liy_yo) - 1}")

    # Detèmine endèks yo menm jan payroll.py fè l
    idx_dat, idx_kolaboratè, idx_kolab_pousantaj = 0, 17, -1
    for i, selil in enumerate(entete):
        selil_clean = selil.strip().upper()
        if "DAT" in selil_clean:
            idx_dat = i
        elif "KOLABORATÈ" in selil_clean or "COLABORATEUR" in selil_clean:
            idx_kolaboratè = i
        elif "%KOLAB" in selil_clean or "% KOLAB" in selil_clean:
            idx_kolab_pousantaj = i
    if idx_kolab_pousantaj == -1:
        for i, selil in enumerate(entete):
            if "KOLAB" in selil.strip().upper():
                idx_kolab_pousantaj = i
                break

    print(f"\n🔍 Endèks detekte otomatikman:")
    print(f"   Dat → kòlòn {chr(ord('A')+idx_dat)} (endèks {idx_dat})")
    print(f"   Kolaboratè → kòlòn {chr(ord('A')+idx_kolaboratè)} (endèks {idx_kolaboratè})")
    print(f"   %Kolab → kòlòn {chr(ord('A')+idx_kolab_pousantaj) if idx_kolab_pousantaj >= 0 else '???'} (endèks {idx_kolab_pousantaj})")

    jodi = date.today()
    limit_dat = jodi - timedelta(days=90)

    print(f"\n📅 Peryòd tès (3 mwa): apati {limit_dat} jiska {jodi}\n")

    print("📄 5 PREMYE LIY DONE (bri, san fòmataj):")
    for n, liy in enumerate(liy_yo[1:6], start=2):
        dat_brit = liy[idx_dat] if len(liy) > idx_dat else None
        dat_pars = pars_dat(dat_brit)
        kolab = liy[idx_kolaboratè] if len(liy) > idx_kolaboratè else None
        kolab_pousantaj = liy[idx_kolab_pousantaj] if idx_kolab_pousantaj >= 0 and len(liy) > idx_kolab_pousantaj else None

        print(f"   Liy {n}: Dat_brit={dat_brit!r} → pars={dat_pars} | "
              f"Kolaboratè={kolab!r} | %Kolab={kolab_pousantaj!r}")

    print("\n💡 Si 'Kolaboratè' oswa '%Kolab' toujou None/vid pou tout liy,")
    print("   sa vle di endèks kòlòn yo pa bon, oswa kòlòn sa yo vid nan Sheets ou a.")


if __name__ == "__main__":
    teste()
