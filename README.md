# JA-GALI — Asistan AI JUST ART

Sistèm ki pèmèt ekip JUST ART (ajans kominikasyon vizyèl) jere pwojè kliyan, peman,
payroll, kontni rezo sosyal, ak rapò — tout atravè yon sèl app (PWA), ki itilize
Claude API pou konprann kòmand an lang natirèl epi aji sou Google Sheets/Docs/
Calendar/Drive ak Notion.

## Estrikti pwojè a

```
JA-GALI/
├── backend/     → API Python (FastAPI) — sèvè a, lojik biznis, entegrasyon API yo
├── app/         → PWA (HTML/CSS/JS) — enstalab sou Android/iOS/tablet
└── docs/        → Kontèks pwojè a ak fèy wout (referans)
```

## Achitekti

```
[PWA — HTML/CSS/JS]
        ↓ (rele API)
[Backend — Python (FastAPI)]
        ↓
[Claude API]
        ↓
[Google Sheets (sous verite) / Docs / Calendar / Drive / Notion / Meta / TikTok]
```

## Kote nou ye

**Faz aktyèl : FAZ 0 — Fondasyon**

Gade `docs/Feuille_de_Route.md` pou detay tout faz yo, ak `docs/Contexte.md` pou
règ biznis kritik yo (kòd pwojè, divizyon 30/70, elatriye).

## Demare backend lan (lokal)

```bash
cd backend
python3 -m venv venv
source venv/bin/activate        # sou Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # epi mete kle API Claude a ladan l
uvicorn main:app --reload
```

Sèvè a ap kouri sou http://localhost:8000 — dokimantasyon otomatik disponib sou
http://localhost:8000/docs

## Teste kle API Claude a (tach 0.6)

```bash
cd backend
python3 test_claude_api.py
```
