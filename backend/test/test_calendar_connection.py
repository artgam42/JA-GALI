"""
Faz 4 — Tès koneksyon Google Calendar.
Kreye yon evènman tès sou Calendar la pou konfime koneksyon an mache.

Itilizasyon:
    python3 test_calendar_connection.py
"""

import os
import sys
from datetime import date, timedelta
from dotenv import load_dotenv

load_dotenv()


def teste():
    fichye_kle = os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE", "service-account.json")
    kal_id = os.getenv("GOOGLE_CALENDAR_ID")

    if not os.path.exists(fichye_kle):
        print(f"❌ Fichye service account pa jwenn: '{fichye_kle}'")
        sys.exit(1)

    if not kal_id:
        print("❌ GOOGLE_CALENDAR_ID pa konfigire nan .env")
        sys.exit(1)

    try:
        from calendar_service import ajoute_delè_pwoje
    except ImportError as e:
        print(f"❌ Enpòte echwe: {e}")
        sys.exit(1)

    dat_tès = date.today() + timedelta(days=1)  # demen, pou pa konfonn ak vrè evènman

    print(f"🔄 M ap kreye yon evènman tès pou dat {dat_tès.strftime('%d/%m/%Y')}...")
    try:
        event_id = ajoute_delè_pwoje("PW26-TEST-Z", dat_tès)
        print(f"✅ Evènman kreye! ID: {event_id}")
        print(f"\n👉 Ale gade Google Calendar ou a — ou dwe wè yon evènman")
        print(f"   '⏰ Delè: PW26-TEST-Z' pou {dat_tès.strftime('%d/%m/%Y')}.")
        print(f"   (Ou ka efase l apre, se te jis yon tès)")
    except Exception as e:
        print(f"❌ Erè: {e}")
        print("\n   Verifye:")
        print("   1. Calendar la pataje ak email service account la (permission 'Make changes to events')")
        print("   2. Google Calendar API aktive nan Google Cloud (tach 0.4)")
        print("   3. GOOGLE_CALENDAR_ID egzat")
        sys.exit(1)


if __name__ == "__main__":
    teste()
