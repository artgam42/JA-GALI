"""
Faz 1.3 — Tès koneksyon Google Sheets.
Ti script sa a konfime service account la ka LI Sheet la (san modifye anyen).

Itilizasyon:
    python3 test_sheets_connection.py
"""

import os
import sys
from dotenv import load_dotenv

load_dotenv()


def teste_koneksyon():
    fichye_kle = os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE", "service-account.json")
    sheet_id = os.getenv("GOOGLE_SHEET_ID")

    if not os.path.exists(fichye_kle):
        print(f"❌ Fichye service account pa jwenn: '{fichye_kle}'")
        print("   → Verifye li nan dosye backend/, epi non li matche .env")
        sys.exit(1)

    if not sheet_id:
        print("❌ GOOGLE_SHEET_ID pa konfigire nan .env")
        sys.exit(1)

    try:
        from sheets_service import li_liy, jwenn_pwochen_liy_vid
    except ImportError as e:
        print(f"❌ Pakèt Google manke: {e}")
        print("   → Lanse: pip install -r requirements.txt")
        sys.exit(1)

    print("🔄 M ap eseye li Journal la...")

    try:
        liy_yo = li_liy("A:G")
        print(f"✅ Koneksyon reyisi! {len(liy_yo)} liy jwenn (ak antèt la).")
        print("\n📋 5 premye liy yo:")
        for i, liy in enumerate(liy_yo[:5]):
            print(f"   Liy {i + 1}: {liy}")

        pwochen = jwenn_pwochen_liy_vid()
        print(f"\n📍 Pwochen liy vid disponib: liy {pwochen}")

    except Exception as e:
        print(f"❌ Erè pandan koneksyon an: {e}")
        print("\n   Verifye:")
        print("   1. Sheet la pataje ak email service account la (aksè Editor)")
        print("   2. Google Sheets API aktive nan Google Cloud (tach 0.4)")
        print("   3. GOOGLE_SHEET_ID egzat (soti nan URL Sheet la)")
        sys.exit(1)


if __name__ == "__main__":
    teste_koneksyon()
