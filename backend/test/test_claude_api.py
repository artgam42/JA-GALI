"""
Faz 0.6 — Premye tès konvèsasyon.
Ti script sa a konfime kle API Claude a byen konfigire epi li mache.

Itilizasyon:
    1. Kreye fichye .env (kopye .env.example) epi mete vrè kle API a ladan l
    2. python3 test_claude_api.py
"""

import os
import sys
from dotenv import load_dotenv

load_dotenv()


def teste_kle_api():
    kle = os.getenv("ANTHROPIC_API_KEY")
    modèl = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-6")

    if not kle or kle.startswith("sk-ant-xxxx"):
        print("❌ Pa gen kle API valid nan fichye .env ou a.")
        print("   → Kopye .env.example rele l .env, epi mete vrè kle a.")
        print("   → Kle a soti sou platform.claude.com (tach 0.2)")
        sys.exit(1)

    try:
        from anthropic import Anthropic
    except ImportError:
        print("❌ Pakèt 'anthropic' pa enstale.")
        print("   → Lanse: pip install -r requirements.txt")
        sys.exit(1)

    print(f"🔄 M ap eseye konekte ak Claude API (modèl: {modèl})...")

    client = Anthropic(api_key=kle)

    try:
        repons = client.messages.create(
            model=modèl,
            max_tokens=100,
            messages=[
                {
                    "role": "user",
                    "content": "Reponn sèlman: 'Kle API a mache byen pou JA-GALI!'",
                }
            ],
        )
        tèks = repons.content[0].text
        print("✅ Koneksyon reyisi!")
        print(f"   Repons Claude: {tèks}")
    except Exception as e:
        print(f"❌ Erè pandan koneksyon an: {e}")
        sys.exit(1)


if __name__ == "__main__":
    teste_kle_api()
