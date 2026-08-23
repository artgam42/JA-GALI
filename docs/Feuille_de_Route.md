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
Yon SÈL kòd aksè pou tout ekip la (pa gen kont endividyèl)
1.3
Konekte ak Google Sheets
Fonksyon Python ki li/ekri sou Sheet "Journal JUST ART" (onglè "Journal Unique 26", deja egziste). Backend ekri sèlman kòlòn "done bri" yo (Dat, Type Opérat., Kliyan/Fournis., Catégorie, Description, Montan, Payer, Kolaboratè) — JANM touche kòlòn fòmil otomatik yo (Solde, Balans Kès, Net/A.Enpr, %JUSTART, %Kolab). Gade Contexte.md §6 pou mapping konplè.
1.4
Lojik kòd pwojè otomatik
Fonksyon ki li Sheets, konte pwojè jou a (parse kòlòn Description), jenere kòd (PW26-816-A, elatriye) selon 3.1
1.5
Ekstraksyon done ak Claude
Claude li mesaj ou ekri an lang natirèl, ekstrè: kliyan, tip travay, infos, delè, kolaboratè, montan. Delè ak Statut sèvi sèlman pou konpoze tèks Description/template Discord (pa estoke kòm kolòn Sheets separe — gade Contexte.md §3.2)
1.6
Kreye antre nan Sheets
Konbine 1.3-1.5: yon mesaj kreye yon liy nan Sheets (kòlòn done bri sèlman) + deklannche premye notifikasyon Discord (Faz 2.3)
1.7
Modifye statiti (⋯ → FINI)
Kòmand pou make yon pwojè fini — PA modifye Sheets (pa gen kolòn Statut), men EDITE mesaj Discord orijinal ki lye ak pwojè a (⋯ → FINI). Mande backend estoke ID mesaj Discord la lyen ak kòd pwojè a pou l ka jwenn li pita (gade Faz 2)
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

FAZ 2 — Notifikasyon Discord (Template Otomatik)
Poukisa touswit apre Faz 1: Fonksyonalite sa a depann sèlman de kreyasyon/modifikasyon pwojè (Faz 1) — li pa mande Payroll, Calendar, ni okenn lòt entegrasyon. Nou fè l vit pou ekip la kòmanse resevwa notifikasyon Discord depi premye pwojè yo antre nan sistèm nan, san bezwen tann rès faz yo.
#
Tach
Sa n ap fè
2.1
Kreye webhook Discord pou chak kalite kliyan
3 webhook separe: Kliyan regilye, Patnè, Kontra — chak nan kanal Discord ki koresponn
2.2
Fonksyon "voye template Discord"
Fonksyon Python ki pran done yon pwojè (kòd, type travay, infos, delè, kolaboratè, statut=⋯) epi fòmate l an yon mesaj klè. Estoke ID mesaj Discord ki retounen an (message_id) yon kote lyen ak kòd pwojè a — nesesè pou 2.3bis
2.3
Konekte ak kreyasyon pwojè (Faz 1.6)
Chak fwa yon nouvo antre pwojè kreye nan Sheets, deklannche otomatikman voye PREMYE template la (statut ⋯) sou bon webhook la (selon kalite kliyan)
2.3bis
Konekte ak modifikasyon statiti (Faz 1.7)
Lè yon pwojè make FINI, EDITE menm mesaj Discord ki te voye nan 2.3 la (pa voye yon nouvo mesaj) — itilize message_id estoke a pou chanje Statut la nan tèks mesaj la (⋯ → FINI)
2.4
Jesyon erè
Si webhook Discord echwe (pa egzanp Discord down), pwojè a dwe toujou kreye/modifye nan Sheets san erè — notifikasyon Discord se yon bonus, pa yon depandans kritik
2.5
Tès ak plizyè kalite kliyan
Kreye yon pwojè pou chak kalite (regilye/patnè/kontra), konfime chak mesaj ateri nan bon kanal Discord, epi konfime edisyon ⋯→FINI mache pou chak

Rezilta faz sa a: Chak fwa yon nouvo pwojè antre nan sistèm nan, tout ekip la wè yon notifikasyon otomatik nan bon kanal Discord — san sistèm nan depann de Discord pou fonksyone.

FAZ 3 — Lajan: Peman, Depans, Payroll
#
Tach
Sa n ap fè
3.1
Estrikti Sheets pou peman
Kolòn pou: montan total, montan peye, rès, statiti peman
3.2
Kòmand "kliyan peye X"
Claude ekstrè montan, modifye Sheets, kalkile rès
3.3
Kòmand "ajoute depans"
Antre yon depans ak kategori/rezon
3.4
Lojik payroll 30/70
Fonksyon ki kalkile pa kolaboratè, ak divizyon selon efò si plizyè moun
3.5
Rapò payroll nan PWA
Yon ti paj/vi nan app la ki montre rezime pa kolaboratè
3.6
Teste ak plizyè senaryo
Yon sèl kolaboratè, plizyè kolaboratè, peman pasyèl

Rezilta faz sa a: Sistèm lan jere tout sik lajan an, e ou ka wè rezime a dirèkteman nan app la.

FAZ 4 — Google Calendar (Alèt nan App la)
Ajisteman enpòtan: Paske ou pa bezwen push notification, alèt yo ap parèt lè ou louvri app la (yon ti "badge" oswa lis "sa k ap vini") olye yo parèt otomatikman sou telefòn ou san ou pa louvri l.
#
Tach
Sa n ap fè
4.1
Konekte ak Calendar API
Fonksyon pou kreye/modifye evènman
4.2
Otomatize evènman travay
Lè yon pwojè kreye (Faz 1), otomatikman ajoute dat kòmansman + dat delè sou Calendar
4.3
Evènman piblikasyon
Evènman separe pou dat/lè yon post gen pou pibliye
4.4
Paj "Alèt" nan PWA
Yon vi nan app la ki montre delè k ap pwoche lè ou louvri l

Rezilta faz sa a: Chak nouvo pwojè otomatikman aparèt sou Calendar, e ou wè yon rezime delè lè ou louvri app la.

FAZ 5 — Kontni: Caption + Notion + Drive
#
Tach
Sa n ap fè
5.1
Konekte ak Notion API
Li done piblikasyon (non, kontèks) nan Notion
5.2
Konekte ak Google Drive
Jwenn/idantifye fichye/imaj ki lye ak yon piblikasyon
5.3
Jenere caption ak Claude
Claude li kontèks Notion + Drive, ekri yon caption apwopriye
5.4
Vi "Caption" nan PWA
Paj kote ou wè caption pwopoze a, ka mande chanjman, aksepte l

Rezilta faz sa a: App la pwopoze caption otomatikman, ou revize/aksepte dirèkteman ladan l.

FAZ 6 — Rapò (Google Docs)
#
Tach
Sa n ap fè
6.1
Konekte ak Google Docs API
Fonksyon pou kreye/ekri nan yon dokiman
6.2
Rasanble done pou rapò
Li Sheets (pwojè, peman, payroll) pou konpile yon rezime
6.3
Jenere rapò ak Claude
Claude ekri yon rapò byen estriktire ak done reyèl yo
6.4
Bouton "Jenere Rapò" nan PWA
Yon senp bouton nan app la ki deklannche kreyasyon rapò a

Rezilta faz sa a: Yon senp klik nan app la jenere yon rapò konplè nan Google Docs.

FAZ 7 — Deplwaman (Fè Tout Bagay Kouri 24/7)
Enpòtan pou PWA: Yon PWA oblije sèvi sou HTTPS (koneksyon sekirize) pou l enstalab — sa vle di ou pa ka tou senpleman "louvri yon fichye" sou telefòn ou, backend AK PWA a dwe ebèje sou entènèt.
#
Tach
Sa n ap fè
7.1
Chwazi ebèjman cloud
Konpare opsyon (Railway, Render, VPS) — dwe sipòte HTTPS otomatikman
7.2
Sekirize kle/sekrè yo
Varyab anviwonman sou sèvè a, pa nan kòd la
7.3
Deplwaye backend la
API la kouri san w pa bezwen limen òdinatè w
7.4
Deplwaye/sèvi PWA a
Fichye HTML/CSS/JS ebèje ak yon domèn HTTPS
7.5
Enstale sou telefòn tout ekip la
Chak moun louvri lyen an, "Add to Home Screen"
7.6
Siveyans ak lòg
Fason pou wè si gen erè san w pa gade tèminal la chak jou
7.7
Tès final an kondisyon reyèl
Ekip la itilize sistèm nan plizyè jou, nou ajiste

Rezilta faz sa a: App la disponib 24/7, tout ekip la enstale l sou telefòn/tablet pa yo.

FAZ 8 — Meta Business + TikTok (Piblikasyon Otomatik)
Poukisa an dènye: Pwosesis apwobasyon Meta/TikTok ka pran plizyè semèn — nou kòmanse demann sa yo an paralèl pandan Faz 4-7 ap kontinye.
#
Tach
Sa n ap fè
8.1
Kreye kont Developer Meta
Soumèt aplikasyon, tann apwobasyon
8.2
Kreye kont Developer TikTok
Soumèt aplikasyon, tann apwobasyon
8.3
Entegre API piblikasyon
Konekte fonksyon piblikasyon ak kontni ki soti Faz 5
8.4
Otomatize sou orè Calendar
Piblikasyon deklannche otomatikman selon evènman Calendar (Faz 4)
8.5
Vi "Piblikasyon" nan PWA
Paj kote ou wè estati chak piblikasyon (planifye/pibliye)
8.6
Tès ak sekirite
Verifye piblikasyon yo kòrèk anvan yo vin totalman otomatik

Rezilta faz sa a: Sistèm nan konplè — soti kreyasyon yon pwojè jiska piblikasyon final la, tout otomatize, tout jere nan yon sèl app.

Rezime Vizyèl
FAZ 0: Fondasyon (kle API, Google Cloud, estrikti /backend + /app)
   ↓
FAZ 1: Backend + Sheets + Premye PWA (KÈ SISTÈM NAN)
   ↓
FAZ 2: Notifikasyon Discord (template otomatik pou chak nouvo pwojè)
   ↓
FAZ 3: Payroll/Lajan
   ↓
FAZ 4: Calendar (alèt nan app)
   ↓
FAZ 5: Caption/Notion/Drive
   ↓
FAZ 6: Rapò Docs
   ↓
FAZ 7: Deplwaman 24/7 (HTTPS obligatwa pou PWA)
   ↓
FAZ 8: Meta/TikTok (demand apwobasyon an paralèl ak Faz 4-7)

Pwen kle pou sonje sou chwa PWA a
Avantaj: Ou kontwole 100% aparans ak konpòtman app la (kontrèman ak Discord), ou itilize konpetans HTML/CSS/JS ou deja genyen, pa gen apwobasyon App Store/Google Play pou tann
Konsekans: Ou dwe bati login/sekirite tèt ou (Discord te fè sa gratis), epi ou bezwen ebèjman HTTPS pou tout bagay mache — sa vin kwit nan Faz 7, men backend la ka rete lokal pandan tès yo (Faz 1-6)

Dokiman sa a se yon referans k ap evolye pandan n ap bati. Nou ka ajiste lòd la si priyorite biznis chanje.
