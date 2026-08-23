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
Otantifikasyon: Login senp (modpas/kòd aksè), paske app la sou entènèt louvri (pa gen kont Discord ki pwoteje l ankò pou LOGIN/ENTÈFAS)
Nòt: Discord PA itilize kòm entèfas sistèm nan ankò, MEN li rete itilize kòm kanal notifikasyon otomatik (voye template chak nouvo pwojè kliyan) — gade Faz 2 nan fèy wout la
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

⚠️ PREMISYON (desizyon Faz 1, valab pou Google Sheet "Journal JUST ART" ki deja egziste):
Delè ak Statut PA estoke kòm kolòn separe nan Google Sheets la. Yo fè pati sèlman
tèks/kontni TEMPLATE DISCORD la (gade Faz 2) — Claude ekstrè yo nan mesaj natirèl
itilizatè a ekri a, yo ale dirèkteman nan mesaj Discord la. Statut swiv sèlman via
edisyon mesaj Discord la (⋯ → FINI), pa gen kolòn Statut nan Sheets. Delè ap konekte
pita ak Google Calendar (Faz 4) kòm sous verite pou dat/echeans.
Kòd, Type Travay, ak Infos yo ekri ansanm nan kòlòn "Description" Sheets la, fòma:
"KÒD : deskripsyon travay la" (egzanp: "PW26-820-A").

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
Piblikasyon otomatik Facebook/Instagram (Faz 8 — apre demand apwobasyon)
TikTok API
Piblikasyon otomatik TikTok (Faz 8 — apre demand apwobasyon)
Claude API
Konprann lang natirèl, ekstrè done, jenere caption/rapò


5. Sa ki DEJA fèt vs sa ki PA ko fèt
⚠️ Enstriksyon pou ajan kodaj la: Anvan ou kòmanse ekri nouvo kòd, mande itilizatè a ki Faz/tach li sou li nan fèy wout la, epi si posib gade fichye pwojè ki deja egziste yo pou w pa refè travay ki deja fèt.
(Itilizatè a: mete yon ti nòt isit chak fwa ou fin yon tach, egzanp: "Faz 1.1-1.4 fin fèt, m sou 1.5 kounye a")

6. Mapping Google Sheet reyèl la ("Journal JUST ART", onglè "Journal Unique 26")
Sheet la deja egziste ak tit/fòmil ki deja fèt — backend lan AJOUTE liy sèlman,
li pa rebati estrikti a.

Kòlòn "done bri" backend lan ekri (input):
Dat | Type Opérat. (Revni/Depans) | Kliyan/Fournis. | Catégorie | Description
(fòma "KÒD : deskripsyon") | Montan | Payer | Kolaboratè

Kòlòn kalkile OTOMATIKMAN pa fòmil Sheets la — backend PA JANM ekri ladan yo:
Solde | Balans Kès | Net/A.Enpr | %JUSTART | %Kolab | Antre Kès | Sòti Kès

Statut peman (3.3: peye total/pasyèl/poko peye) li deja kouvri pa kòlòn "Solde"
(0 = peye total).

7. Dokiman konplemantè
Fèy wout konplè (Feuille_de_Route.md) — lis tout faz ak tach yo an detay
Dokiman sa a — kontèks jeneral pou chak sesyon kodaj
