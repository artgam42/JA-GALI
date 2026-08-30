"""
Faz 6 — Tès koneksyon Google Docs (SAN Claude).
Kreye yon dokiman tès ak tèks senmile, pou konfime koneksyon
Docs+Drive lan mache — anvan nou gen kredi pou vrè jenerasyon Claude.

Itilizasyon:
    python3 test_docs_connection.py
"""

import os
import sys
from dotenv import load_dotenv

load_dotenv()


def teste():
    fichye_kle = os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE", "service-account.json")
    dosye_id = os.getenv("GOOGLE_DRIVE_DOSYE_RAPÒ_ID")

    if not os.path.exists(fichye_kle):
        print(f"❌ Fichye service account pa jwenn: '{fichye_kle}'")
        sys.exit(1)

    if not dosye_id:
        print("❌ GOOGLE_DRIVE_DOSYE_RAPÒ_ID pa konfigire nan .env")
        sys.exit(1)

    try:
        from docs_service import kreye_rapò
    except ImportError as e:
        print(f"❌ Enpòte echwe: {e}")
        print("   → pip install -r requirements.txt")
        sys.exit(1)

    tèks_senmile = (
        "RAPÒ TÈS — JA-GALI\n\n"
        "Sa a se yon dokiman TÈS otomatik, pou konfime koneksyon Google "
        "Docs + Drive mache kòrèkteman.\n\n"
        "Kantite pwojè (senmile): 5\n"
        "Total revni (senmile): 25,000 goud\n"
        "Total depans (senmile): 3,500 goud\n\n"
        "Si w wè tèks sa a byen fòmate nan Google Docs, koneksyon an reyisi! "
        "Ou ka efase dokiman sa a apre, se te jis yon tès."
    )

    print("🔄 M ap kreye yon dokiman tès nan dosye rapò a...")
    try:
        rezilta = kreye_rapò("🧪 Rapò TÈS — JA-GALI", tèks_senmile)
        print(f"✅ Dokiman kreye!")
        print(f"   ID: {rezilta['id']}")
        print(f"   Lyen: {rezilta['lyen']}")
        print(f"\n👉 Ale klike lyen anwo a pou konfime dokiman an gen tèks ladan l.")
    except Exception as e:
        print(f"❌ Erè: {e}")
        print("\n   Verifye:")
        print("   1. Dosye rapò a pataje ak email service account la kòm 'Editor'")
        print("   2. Google Docs API AK Google Drive API tou de aktive nan Google Cloud")
        print("   3. GOOGLE_DRIVE_DOSYE_RAPÒ_ID egzat")
        sys.exit(1)


if __name__ == "__main__":
    teste()
