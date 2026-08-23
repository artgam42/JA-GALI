Kontèks Pwojè — Asistan AI JUST ART

1. Rezime an yon fraz
Yon sistèm ki pèmèt ekip JUST ART (ajans kominikasyon vizyèl) jere pwojè kliyan, peman, payroll, kontni rezo sosyal, ak rapò — tout atravè yon sèl app (PWA), ki itilize Claude API pou konprann kòmand an lang natirèl epi aji sou Google Sheets/Docs/Calendar/Drive ak Notion.

2. Achitekti teknik
[PWA — HTML/CSS/JS, enstalab sou Android/iOS/tablet]
              ↓ (rele API)
[Backend — Python (FastAPI)]
              ↓
[Claude API — konprann kòmand, ekstrè done, jenere tèks]
              ↓
[Google Sheets (sous verite), Google Docs, Google Calendar, Google Drive, Notion, Meta Business Suite, TikTok]

Backend: Python + FastAPI, ebèje sou cloud (HTTPS obligatwa pou PWA a)
Frontend: PWA — HTML/CSS/JS, ak manifest.json + service worker pou enstalasyon
Otantifikasyon: Login senp (modpas/kòd aksè), paske app la sou entènèt louvri (pa gen kont Discord ki pwoteje l ankò)
"Sous verite" pou done yo: Google Sheets — backend lan dwe toujou li Sheets anvan pou konnen eta reyèl la (pa fè sipozisyon)
Notifikasyon: Pa gen push — alèt parèt kòm yon vi/paj lè itilizatè a louvri app la

3. Règ biznis kritik (pa neglije sa yo)
3.1 Sistèm kòd pwojè
Kalite kliyan
Fòma
Egzanp
Kliyan regilye
PW[ane 2-chif][mwa][jou]-[lèt sekans]
PW26-816-A = 2026, mwa 8, jou 16, 1e pwojè jou a
Patnè
JA-P[nimewo]-[dat]-[lèt]
JA-P005-701A
Kontra
JA-C[nimewo]-[dat]-[lèt]
JA-C004-620A

Enpòtan: Lèt sekans lan (A, B, C...) depann de konbyen pwojè ki deja kreye pou dat/kliyan sa a — backend lan dwe li Sheets anvan pou konte epi jenere bon lèt la.
3.2 Chan yo pou chak antre pwojè
Kòd (jenere otomatikman selon 3.1)
Type Travay
Infos (deskripsyon travay la)
Delè (dat pou remèt)
Kolaboratè (ki moun k ap reyalize — souvan Manager a limenm)
Statut (⋯ pandan l ap fèt → FINI lè l fini)
3.3 Peman ak Payroll
Chak pwojè gen yon statiti peman: peye total, peye pasyèl (rès poko peye), oswa poko peye ditou
Divizyon lajan: 30% pou JUST ART, 70% pou kolaboratè(s)
Si plizyè kolaboratè travay sou menm pwojè a: 70% la separe selon efò chak moun, pa egal-egal otomatikman
Depans (achte materyèl, elatriye) yo antre epi kategorize apa

4. Entegrasyon (API) yo itilize
Sèvis
Itilizasyon
Google Sheets API
Sous verite: pwojè, peman, payroll, depans
Google Docs API
Jenere rapò otomatik
Google Calendar API
Evènman pou delè travay ak dat piblikasyon
Google Drive API
Jwenn imaj/fichye ki lye ak yon piblikasyon
Notion API
Kontèks/deskripsyon pou jenerasyon caption
Meta Business Suite API
Piblikasyon otomatik Facebook/Instagram (Faz 7 — dènye)
TikTok API
Piblikasyon otomatik TikTok (Faz 7 — dènye)
Claude API
Konprann lang natirèl, ekstrè done, jenere caption/rapò


5. Sa ki DEJA fèt vs sa ki PA ko fèt
⚠️ Enstriksyon pou ajan kodaj la: Anvan ou kòmanse ekri nouvo kòd, mande itilizatè a ki Faz/tach li sou li nan fèy wout la, epi si posib gade fichye pwojè ki deja egziste yo pou w pa refè travay ki deja fèt.
(Itilizatè a: mete yon ti nòt isit chak fwa ou fin yon tach, egzanp: "Faz 1.1-1.4 fin fèt, m sou 1.5 kounye a")

6. Dokiman konplemantè
Fèy wout konplè (feuille-de-route-just-art-assistant.md) — lis tout faz ak tach yo an detay
Dokiman sa a — kontèks jeneral pou chak sesyon kodaj
