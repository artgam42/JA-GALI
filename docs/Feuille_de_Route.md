FEUILLE DE ROUTE

Fèy Wout — Asistan AI pou JUST ART (Vèsyon PWA)
Apwòch: 100% kòd pwòp tèt — Backend Python + PWA (app web enstalab) Editè: Antigravity (IDE agantik, similè VS Code) Rit travay: Prèske tan plen Entèfas: App pwòp tèt ou, enstalab sou Android/iOS/tablet — PA Discord Notifikasyon: Pa gen push obligatwa — team lan louvri app la pou tcheke

FAZ 0 — Fondasyon
Objektif: Prepare tout zouti ak aksè anvan n ekri premye liy kòd metye.
#
Tach
Sa n ap fè
0.1
Enstale anviwonman devlopman
Python, Antigravity, Git
0.2
Kreye kont API Claude
platform.claude.com, kle API, plafon depans
0.3
Estriktire pwojè a
De dosye separe: /backend (Python) ak /app (PWA: HTML/CSS/JS)
0.4
Google Cloud + API
Aktive Sheets, Docs, Calendar, Drive API; kreye "service account"
0.5
Chwazi "framework" backend
FastAPI (rekòmande — modèn, rapid, fasil dokimante otomatikman)
0.6
Premye tès konvèsasyon
Yon ti script ki konfime kle API Claude a mache

Rezilta faz sa a: Yon pwojè vid men byen estriktire, ak tout kle/aksè ki mache.

FAZ 1 — Backend debaz + Sheets + Premye vèsyon PWA
Poukisa an premye: Sa a se kè sistèm nan. Backend la ak Sheets ap sèvi kòm fondasyon pou tout rès sistèm nan; PWA a se fenèt ou ap gade tout bagay ladan.
#
Tach
Sa n ap fè
1.1
Kreye API backend debaz
Yon sèvè FastAPI ki resevwa mesaj, retounen repons
1.2
Otantifikasyon senp
Login ak modpas (oswa kòd aksè) pou team lan sèl ka itilize app la
1.3
Konekte ak Google Sheets
Fonksyon Python ki li/ekri sou yon sheet
1.4
Lojik kòd pwojè otomatik
Fonksyon ki li Sheets, konte pwojè jou a, jenere kòd (PW26-816-A, elatriye)
1.5
Ekstraksyon done ak Claude
Claude li mesaj ou ekri an lang natirèl, ekstrè: kliyan, tip travay, enfo, delè, kolaboratè
1.6
Kreye antre nan Sheets
Konbine 1.3-1.5: yon mesaj kreye yon liy nan Sheets
1.7
Modifye statiti (⋯ → FINI)
Kòmand pou modifye yon pwojè ki egziste deja
1.8
Premye vèsyon PWA
Paj login + yon chat senp (HTML/CSS/JS) ki rele API backend la
1.9
manifest.json + service worker
Fè app la enstalab sou telefòn/tablet
1.10
Teste bout an bout sou telefòn
Enstale app la sou telefòn ou, kreye pwojè tès, verifye Sheets senkwonize

Rezilta faz sa a: Ou gen yon app sou telefòn ou kote ou ka ekri yon kòmand, li kreye/modifye yon liy nan Sheets.

FAZ 2 — Lajan: Peman, Depans, Payroll
#
Tach
Sa n ap fè
2.1
Estrikti Sheets pou peman
Kolòn pou: montan total, montan peye, rès, statiti peman
2.2
Kòmand "kliyan peye X"
Claude ekstrè montan, modifye Sheets, kalkile rès
2.3
Kòmand "ajoute depans"
Antre yon depans ak kategori/rezon
2.4
Lojik payroll 30/70
Fonksyon ki kalkile pa kolaboratè, ak divizyon selon efò si plizyè moun
2.5
Rapò payroll nan PWA
Yon ti paj/vi nan app la ki montre rezime pa kolaboratè
2.6
Teste ak plizyè senaryo
Yon sèl kolaboratè, plizyè kolaboratè, peman pasyèl

Rezilta faz sa a: Sistèm lan jere tout sik lajan an, e ou ka wè rezime a dirèkteman nan app la.

FAZ 3 — Google Calendar (Alèt nan App la)
Ajisteman enpòtan: Paske ou pa bezwen push notification, alèt yo ap parèt lè ou louvri app la (yon ti "badge" oswa lis "sa k ap vini") olye yo parèt otomatikman sou telefòn ou san ou pa louvri l.
#
Tach
Sa n ap fè
3.1
Konekte ak Calendar API
Fonksyon pou kreye/modifye evènman
3.2
Otomatize evènman travay
Lè yon pwojè kreye (Faz 1), otomatikman ajoute dat kòmansman + dat delè sou Calendar
3.3
Evènman piblikasyon
Evènman separe pou dat/lè yon post gen pou pibliye
3.4
Paj "Alèt" nan PWA
Yon vi nan app la ki montre delè k ap pwoche lè ou louvri l

Rezilta faz sa a: Chak nouvo pwojè otomatikman aparèt sou Calendar, e ou wè yon rezime delè lè ou louvri app la.

FAZ 4 — Kontni: Caption + Notion + Drive
#
Tach
Sa n ap fè
4.1
Konekte ak Notion API
Li done piblikasyon (non, kontèks) nan Notion
4.2
Konekte ak Google Drive
Jwenn/idantifye fichye/imaj ki lye ak yon piblikasyon
4.3
Jenere caption ak Claude
Claude li kontèks Notion + Drive, ekri yon caption apwopriye
4.4
Vi "Caption" nan PWA
Paj kote ou wè caption pwopoze a, ka mande chanjman, aksepte l

Rezilta faz sa a: App la pwopoze caption otomatikman, ou revize/aksepte dirèkteman ladan l.

FAZ 5 — Rapò (Google Docs)
#
Tach
Sa n ap fè
5.1
Konekte ak Google Docs API
Fonksyon pou kreye/ekri nan yon dokiman
5.2
Rasanble done pou rapò
Li Sheets (pwojè, peman, payroll) pou konpile yon rezime
5.3
Jenere rapò ak Claude
Claude ekri yon rapò byen estriktire ak done reyèl yo
5.4
Bouton "Jenere Rapò" nan PWA
Yon senp bouton nan app la ki deklannche kreyasyon rapò a

Rezilta faz sa a: Yon senp klik nan app la jenere yon rapò konplè nan Google Docs.

FAZ 6 — Deplwaman (Fè Tout Bagay Kouri 24/7)
Enpòtan pou PWA: Yon PWA oblije sèvi sou HTTPS (koneksyon sekirize) pou l enstalab — sa vle di ou pa ka tou senpleman "louvri yon fichye" sou telefòn ou, backend AK PWA a dwe ebèje sou entènèt.
#
Tach
Sa n ap fè
6.1
Chwazi ebèjman cloud
Konpare opsyon (Railway, Render, VPS) — dwe sipòte HTTPS otomatikman
6.2
Sekirize kle/sekrè yo
Varyab anviwonman sou sèvè a, pa nan kòd la
6.3
Deplwaye backend la
API la kouri san w pa bezwen limen òdinatè w
6.4
Deplwaye/sèvi PWA a
Fichye HTML/CSS/JS ebèje ak yon domèn HTTPS
6.5
Enstale sou telefòn tout ekip la
Chak moun louvri lyen an, "Add to Home Screen"
6.6
Siveyans ak lòg
Fason pou wè si gen erè san w pa gade tèminal la chak jou
6.7
Tès final an kondisyon reyèl
Ekip la itilize sistèm nan plizyè jou, nou ajiste

Rezilta faz sa a: App la disponib 24/7, tout ekip la enstale l sou telefòn/tablet pa yo.

FAZ 7 — Meta Business + TikTok (Piblikasyon Otomatik)
Poukisa an dènye: Pwosesis apwobasyon Meta/TikTok ka pran plizyè semèn — nou kòmanse demann sa yo an paralèl pandan Faz 3-6 ap kontinye.
#
Tach
Sa n ap fè
7.1
Kreye kont Developer Meta
Soumèt aplikasyon, tann apwobasyon
7.2
Kreye kont Developer TikTok
Soumèt aplikasyon, tann apwobasyon
7.3
Entegre API piblikasyon
Konekte fonksyon piblikasyon ak kontni ki soti Faz 4
7.4
Otomatize sou orè Calendar
Piblikasyon deklannche otomatikman selon evènman Calendar (Faz 3)
7.5
Vi "Piblikasyon" nan PWA
Paj kote ou wè estati chak piblikasyon (planifye/pibliye)
7.6
Tès ak sekirite
Verifye piblikasyon yo kòrèk anvan yo vin totalman otomatik

Rezilta faz sa a: Sistèm nan konplè — soti kreyasyon yon pwojè jiska piblikasyon final la, tout otomatize, tout jere nan yon sèl app.

Rezime Vizyèl
FAZ 0: Fondasyon (kle API, Google Cloud, estrikti /backend + /app)
   ↓
FAZ 1: Backend + Sheets + Premye PWA (KÈ SISTÈM NAN)
   ↓
FAZ 2: Payroll/Lajan
   ↓
FAZ 3: Calendar (alèt nan app)
   ↓
FAZ 4: Caption/Notion/Drive
   ↓
FAZ 5: Rapò Docs
   ↓
FAZ 6: Deplwaman 24/7 (HTTPS obligatwa pou PWA)
   ↓
FAZ 7: Meta/TikTok (demand apwobasyon an paralèl ak Faz 3-6)

Pwen kle pou sonje sou chwa PWA a
Avantaj: Ou kontwole 100% aparans ak konpòtman app la (kontrèman ak Discord), ou itilize konpetans HTML/CSS/JS ou deja genyen, pa gen apwobasyon App Store/Google Play pou tann
Konsekans: Ou dwe bati login/sekirite tèt ou (Discord te fè sa gratis), epi ou bezwen ebèjman HTTPS pou tout bagay mache — sa vin kwit nan Faz 6, men backend la ka rete lokal pandan tès yo (Faz 1-5)

Dokiman sa a se yon referans k ap evolye pandan n ap bati. Nou ka ajiste lòd la si priyorite biznis chanje.
