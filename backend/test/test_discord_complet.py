"""
Faz 2 — Tès konplè Discord: voye premye mesaj, estoke message_id, edite pou FINI.

Sa a rele fonksyon yo DIRÈKTEMAN (pa atravè /chat), paske Faz 1.5/1.6
(ekstraksyon Claude) poko fèt — nou senmile done yon "nouvo pwojè" a lamen.

Itilizasyon:
    python3 test_discord_complet.py
"""

import os
import sys
from datetime import date
from dotenv import load_dotenv

load_dotenv()


def teste():
    try:
        from discord_service import voye_notifikasyon_nouvo_pwoje, edite_mesaj_fini
        from sheets_service import estoke_message_id
    except ImportError as e:
        print(f"❌ Enpòte echwe: {e}")
        print("   → pip install -r requirements.txt")
        sys.exit(1)

    # Kòd tès la — dat jodi a, kliyan regilye
    jodi = date.today()
    kòd_tès = f"PW{jodi.strftime('%y')}-{jodi.month}{jodi.day:02d}-TEST"

    print(f"🔄 Etap 1/3 — M ap voye premye mesaj Discord pou '{kòd_tès}'...")
    try:
        message_id = voye_notifikasyon_nouvo_pwoje(
            kòd=kòd_tès,
            type_travay="Tès Faz 2",
            infos="Sa a se yon mesaj tès otomatik pou konfime koneksyon Discord.",
            delè="Pa gen (tès)",
            kolaboratè="Script tès",
        )
        print(f"✅ Mesaj voye! message_id = {message_id}")
    except Exception as e:
        print(f"❌ Erè pandan voye mesaj la: {e}")
        print("   → Verifye DISCORD_WEBHOOK_REGILYE nan .env")
        sys.exit(1)

    print(f"\n🔄 Etap 2/3 — M ap estoke message_id nan onglè Discord_IDs...")
    try:
        estoke_message_id(kòd_tès, message_id)
        print("✅ Estoke nan Sheets!")
    except Exception as e:
        print(f"❌ Erè pandan estoke: {e}")
        sys.exit(1)

    input("\n👉 Ale gade Discord kounye a pou konfime mesaj la la, epi peze Enter pou kontinye...")

    print(f"\n🔄 Etap 3/3 — M ap edite mesaj la pou FINI...")
    try:
        edite_mesaj_fini(kòd_tès, message_id)
        print("✅ Mesaj edite!")
    except Exception as e:
        print(f"❌ Erè pandan edisyon: {e}")
        sys.exit(1)

    print("\n🎉 TÈS KONPLÈ REYISI! Ale verifye mesaj Discord la montre 'FINI' kounye a.")


if __name__ == "__main__":
    teste()
