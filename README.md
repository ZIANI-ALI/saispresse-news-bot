# News bot (Telegram + Gemini)

Kayraqeb ~24 source dyal l akhbar f l Maghrib kol 60 tanya. Kol khabar jdid = **message wa7d (card)** f Telegram:

1. **Cover kbira** + header (score, source, sa3a, 3onwan, lien) + ma3loumat 3la tswira (7orra wla copyright, credit).
2. **◀ 1/3 ▶**: kat9leb bin covers (tswira d source, chakhsiya, tsawer 7orra) f nefs l message.
3. **✅ Valider had l cover** → toggles **✅ Site / ✅ Post** (3alama l9eddam). **📱 Story** dima kayji f pack (b l yed), bla bouton.
4. **📦 Pack final** → reply b fichiers quality kamla: cover 4:5 (Post), tswira 16:9 (Site), story 9:16 (tswira l fo9, panel navy b catégorie, titre f l wost, logo w lta7t **blasa khawya l sticker d lien** (cadre dahbi 380×128 b nefs proportion d sticker, kbbro 7tta y3mmro, + flèches lta7t (click, machi swipe up): Instagram ma kaykhallich tkhbbi sticker, donc kayban b7al bouton d design; ktb fih «التفاصيل»); match/chi3arat: cover f l wost), w nsous jahzin l copie: **النسخة 1** (l site) w **Caption** d Instagram. Compteur d lyoum kayban (API Instagram: max 50 post+story f 24h).
   **🌐 Site automatique** (ila kaynin `SITE_PUBLISH_URL` f Variables = `https://saispress.com/api/bot/publish` w `BOT_PUBLISH_SECRET` f Secrets, nefs secret li f hPanel): Publier kaynchr l article **direct** f saispress.com (3onwan + النسخة 1 + المصدر + credit d tswira 7orra + tswira 16:9 1600×900 + ركن + SEO auto) b **ta2kid** 9bel, w lien d article kayban f card. Ma kaytnchrch joj mrat. Ila site ma jawebch: tswira w النسخة 1 kayjiw f Pack b7al 9bel.
   **📸 Instagram automatique** (ila kaynin secret `IG_ACCESS_TOKEN` w variable `IG_USER_ID`, m3a Site configuré): bouton wlla **🚀 Publier** → **ta2kid** (✅ Nchr daba / ❌ Rj3) → Site (direct) w **Post** (cover 4:5 + caption + المصدر + credit d tswira) kaytnchro b API rasmi (Instagram API with Instagram Login). Tswira katmchi l site (`/api/bot/media`) 7it Instagram kayjibha b URL public. **📱 Story 🔗**: API ma kaysm7ch b sticker d lien, donc story (9:16) katji f reply m3a **lien 9sir d article** (`https://saispress.com/news/<id>`: slug 3arabi twil bzaf l sticker; site kayredirecti l article) → nchrha mn app Instagram w zid sticker 🔗 3la «التفاصيل». Card katban lien d post w quota l7a9i9i (x/50 f 24h); ila quota ma kafyach wla Instagram rfed, Post kayji f Pack b l yed. **🔁 Pack 3awtani** = fichiers bo7dhom, bla nchr 3awtani. Ila Instagram ma 9derch yjib tswira (code 9004: nginx d Hostinger kayrja3 chi merrat `307` l nefs l lien), bot kay9ra tswira 7tta tji 200 (CDN kaykhbbiha) w kay3awd 7tta 5 mrat (~50 s); ila b9a, Post kayji f Pack. Token kaydoum 60 youm: bot kaytmddo 9bel ma ysali b 10 iyam, w ila ma tmddch kaynbhek f Telegram (token ma kaytkhzen f ta state).
   **🖼 Tswira d site** (mor ✅): preview 16:9 b7al site, ◀ ▶ bin ga3 tsawer d l khabar, **✂️ M9tou3a** (16:9) wla **🔲 Kamla** (tswira kamla bla 9ta3, jnab mdbblin: l tsawer twila), **✅ Hadi l site**. Bla had l ikhtiyar: site katakhod tswira d cover m9tou3a. Kol wa7da mn Site / Post / Story katnchr ghir ila fiha ✅.
5. **📄 النسخة 1 / 📝 Caption**: kaytsiftou ghir ila clickiti. **↩️ Bddel cover** kayrj3ek l ikhtiyar.

Covers kaytkhzno f Telegram (file_id) w cards f `state/cards.json` (3 iyam). Boutons kayjiw b `getUpdates` f thread bo7dha: click bin run w run (~1-2 d9aye9) kaytsna 7tta ybda run jay. Ila bot 3ndo webhook (wla bot akhor kaysta3mel nefs token), Telegram kayrfed getUpdates (409) w bot kaysifet tnbih wa7d f nhar. `EDITOR_IDS` (Variables, ikhtiyari): IDs li y9dro yclickiw; khawi = ay wa7d f chat. A7san chat ykoun private: `TELEGRAM_CHAT_ID` = ID dyalk.

Ila Gemini ma jawebch (quota): card katsifet b tswira d source + "⏳", w mlli yjawb kattkml **nefs l card** (covers + nsous). Khabar wsel ghir b 3onwan: covers mn l 3onwan, w mlli ywsel nass mn source okhra kayttzad f nefs l card (+ message sghir "📄 النص الكامل وصل").

**Ghir l mohim:** Gemini kay3ti l kol khabar note d ahamiya mn 10. Kolchi li 3ndo `MIN_SCORE` (8) wla ktar kaytsifet bla 7add (bla limite f sa3a). `HIGH_SCORE` (8): ghir l 9-10 (> 8) kaykounou 3ajil. Tqder tbdel had l ar9am men Variables.

**Akhbar dawliya:** sources b `"intl": true` (سكاي نيوز عربية، بي بي سي عربي; الجزيرة w فرانس 24 m7bousin: feed bati2). Khabar dawli kaytsifet b7al l akhrin: score >= `MIN_SCORE` (8).

**Kora:** sources رياضة (هسبورت، سكاي نيوز عربية رياضة، ماركا ريال مدريد/برشلونة، آس، موندو ديبورتيفو برشلونة/ريال مدريد). Gemini (judge) kay3ref l khabar dyal kora (`football`) w kay3tih score b slom khas: 8 = natija d l mountakhab, ay match d l Botola, l fera9 l maghribiya f Afri9ya, l mountakhabat l kbar, transfer d la3ib maghribi wla star, akhbar kbar d Real/Barça; 7 = akhbar Real/Barça dyal Marca, akhbar l fera9 l maghribiya, la3ibin maghariba f Oropa. Kora kattsifet mn 7+ 7tta ila kant dawliya.

**Khabar bla nass** (Google News / site kayblocki): ma kaytsiftsh; bot kaytsna 7tta source okhra tjib nafs l khabar b l article, w 3ad kaysifeto kamel (cover + النسخة 1/2). Ghir ila score 9-10: kaytsifet daba b cover men l 3onwan bark (bla versions), w mnin ywsel l article men source okhra kaytsifet tani kamel ("📄 النص الكامل وصل").

**Kol khabar:** tswira + 3onwan asli (+ note) → النسخة 1 → Instagram (3onwan viral + 2-3 fiqrat). Kol khabar kaybda b khatt fasel w ra9mo f nhar.

**Tsawer 7orra (Pexels / Pixabay / Openverse):** Gemini kay3ti 3 recherches (mn d9i9a l 3amma, b7al `bone in red dirt | skull buried soil | crime scene tape`); l kol wa7da kayjereb Pexels/Pixabay, w ila walou Openverse (majjani bla key: Flickr, Wikimedia; ghir CC0/PDM/BY/BY-SA). Tsawer d Openverse kayjiw b credit w licence; BY-SA kat3ni cover khasso nafs l licence. Mn b3d, bot kayjme3 7tta ~18 tswira (2 mn kol source l kol recherche) w kaysifethom sghar l Gemini, li kay3ti **score 0-10** l kol tswira 3la 7sab 3ala9tha b had l khabar bdat (machi b l majal l 3am); ghir li 3ndhom **≥ 7** (`IMG_MIN_SCORE`) kaydkhlo l covers (max 2, mn l a7san). A3lam/ma3alim d dwal okhra, mnadir machi mn lmghrib l khabar maghribi, nas, w tsawer 3amma (sma, zn9a, ml3ab khawi) kayakhdo score sghir. Ila 7tta wa7da ma wslat 7 (wla Gemini ma jawebch), ma kayjich cover b tswira 7orra: tswira bla 3ala9a a9b7 mn bla tswira. Ma kayn ta recherche 3amma mn category. **Tswira d source = référence:** Gemini kaychouf tswira d l article m3a tsawer 7orra: li kayshbhou l mchhed dyalha (nefs naw3 l mkan / l 7adat / l achya2) kayakhdo score ktar, w kay3ti `photo_query` (b7ath kayweṣf l mchhed d tswira). Ila 7tta tswira 7orra ma wslat 7 (w ma kaynach chakhsiya), bot kay3awd yb7th b `photo_query` w Gemini kay9arn b tswira d source (call wa7d zayed, ghir f had l 7ala). Recherches f Pexels/Pixabay/Openverse kaytlanceaw f nefs l w9t. Wikimedia: kayst3mel thumbs (1920px) b User-Agent wad7, 7it l original kayrja3 429. zid secret `PIXABAY_API_KEY` (majjani, l key kayban f https://pixabay.com/api/docs/ men b3d login) wla `PEXELS_API_KEY` (https://www.pexels.com/api/, daba mwe99fin keys jdad). Ila kaynin b jouj, Pexels lowel w Pixabay ila ma l9a walou. Kol khabar kayjih tswira HD bla copyright (cover 4:5 + site 16:9), mkhtara 3la 7sab l mawdou3. Tswira d l source katb9a référence bark.
**Khabar f lmghrib** (Morocco f recherches d Gemini): ghir tsawer li l bank kaygoul bli mn lmghrib (Morocco / Maroc / mdina maghribiya f titre, tags wla description; Pexels: alt + lien). Ila ma kayna 7tta wa7da mn lmghrib, kayb9aw l khrin (w score ≥ 7 kayfrez). **Quality:** Pexels `large`, Pixabay ≥ 1920px, Openverse ≥ 1600×900.
**Tswira mnchoura ma t3awedch:** kol tswira tnchrat (🚀 Publier: cover d Post/Story w tswira d Site) kat9yed b basma (dhash) f `cards.json`; f nefs nhar (Casablanca) ma kat9tar7ch 3awtani f ay card (source, chakhsiya, 7orra, idara), 7tta ila jat mn source okhra wla b 9yas khor.
**Category:** dima wa7da mn 12 (سياسة، اقتصاد، مجتمع، حوادث، رياضة، دولي، ثقافة، صحة، تعليم، طقس، تكنولوجيا، فن). Ila Gemini kteb chi ghalat (b7al «طوقس»), bot kay9addo l a9rab wa7da (طقس); ila ma t3erfatch, cover bla catégorie w site «مجتمع».

**Bla tkrar:** nafs l khabar men sources mkhtalfin kaywsel mra we7da (l source lowla). Ila 3onwan tchabeh, Gemini kayqarer wach nafs l 7adath wla tatawor jdid.

**Rapport youmi (22:00):** tartib dyal sources 3la 7sab chkoun jab l khbar lowl f 7 iyam lkhrin. Sta3mlo bach t7bes sources li ma kayzidou walou.

Sources: `sources.json` (`enabled: false` bach t7bes wa7ed). Sites li kaybloquiw RSS (Le360, SNRT, Hibapress, Chouf...) kaydouzo b Google News: kaywsel ghir 3onwan + lien, bla versions.

## Setup (mra we7da)

1. **Bot Telegram**: f Telegram 9leb `@BotFather` → `/newbot` → khod l token.
2. **Chat ID**: sifet ay message l bot dyalk, men b3d 7el `https://api.telegram.org/bot<TOKEN>/getUpdates` → `"chat":{"id": ...}`.
3. **Gemini key**: https://aistudio.google.com/apikey → Create API key (free).
4. **GitHub Secrets**: repo → Settings → Secrets and variables → Actions → *New repository secret*:
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHAT_ID`
   - `GEMINI_API_KEY`
5. **Test**: Actions → *News bot* → *Run workflow* (5 d9aye9). Awel dowra katsifet "✅ Bot khdam" w ma katsifetsh l akhbar l 9dam.
6. **Tkhdem 24/24**: tab *Variables* → `NEWS_BOT_ENABLED` = `true`, men b3d *Run workflow* mra we7da. Kol run melli ysali kay-lanci run jay bo7do. Bach t7bso: `NEWS_BOT_ENABLED` = `false`.

Variables ikhtiyariyin: `MIN_SCORE`, `HIGH_SCORE`, `GEMINI_MODELS`, `POLL_SECONDS`, `RUN_MINUTES`, `EDITOR_IDS`, `SITE_PUBLISH_URL` (+ secret `BOT_PUBLISH_SECRET`), `IG_USER_ID` (+ secret `IG_ACCESS_TOKEN`).

## Mohim

- Repo public: d9aye9 GitHub Actions bla 7did, free. L keys f Secrets, ma kayban walou.
- GitHub kaytfi l workflows `schedule` ila ma kan 7ta commit 60 youm. Dir commit sghir mra f chhar (mthal bdel `sources.json`).

## Limites Gemini free

Free tier 3ndo limite d requests f l youm, w kol model 3ndo quota dyalo. Ktaba (w ikhtiyar d tsawer) b models `flash` (a7dath 9bel) **ghir l akhbar lmohimmin**: score 9-10 wla 3ajil, wla fihom l malik / l polis (DGSN) / wizara wla wazir (f l 3onwan wla bdyat nass). Lbaqi kaytkteb b `flash-lite` bark (500 f nhar l kol model) bach quota d flash (free: 20 call f nhar l kol model) tb9a l lmohimmin. Ila quota d flash salat, l mohimmin 7tta homa kaydouzo l `flash-lite`. Kol post mktoub b lite kayttmerka **⚠️ [lite]** f النسخة 1 w f cover bach traje3 l3arbiya 9bel ma tnchr. **Judge** kaykhdem b `flash-lite` 9bel (quota dyalo bo7do: free tier d flash = ~20 call f nhar l kol model), w ila salat lite kaydouz l flash; model li rja3 429 kayt7bes (1 min ila quota d d9i9a; ila quota d nhar, 7tta nos lil d California = 08:00 Maghrib f sif, 09:00 f chta) w kaydouz l li mor. Rapport d 22:00 kayban ch7al d call Gemini (judge / ktaba / tsawer) w ch7al nej7o w ch7al rj3o quota l kol model.

**Ila quota salat (wla model 3amer):** bot kaydouz dghya l model li mor (a7dath 9bel: 3.8 → 3.7 → … flash, mn b3d lite) w kaykmmel l khdma. Akhbar 3adiyin w judge kaybdaw b lite, w ila lite salaw wla "high demand" (5xx) kaydouzo l flash. 5xx: mra tanya mor 10 s, w ila 3awd fshel dak l model kaytsedd 2 d9aye9. Models li quota dyalhom d nhar salat kaytkhznou f state (`gemini_cd`), donc run jay ma kay3awdch yjarbhom 7tta yrj3o. Rate limit (`GEMINI_MIN_INTERVAL`) kayt7seb l kol model bo7do. Ghir ila salaw kolchi models: l khabar kaydkhol queue d retry (7tta 12 sa3a).

**Call wa7d l kol post:** judge (b l groupe) kay3ti m3a score: category, recherches d tswira, w smiya d chakhsiya. Bot kayjme3 tsawer (chakhsiya mn Openverse + ta3biriya) 9bel l ktaba, w Gemini kaykteb l versions w kaykhtar tswira f nafs l call (`person_choice`, `image_choice`). Khabar bla hints (9dim f queue): ikhtiyar d tswira f call bo7do b7al 9bel.

**Judge b l groupe:** akhbar jdad kaytsnaw `JUDGE_WAIT` (300s = 5 d9aye9) f queue, men ba3d Gemini kayjudgihom f call wa7d (7tta `JUDGE_BATCH` = 15 khabar). F nafs l call kaychouf 3anawin d ga3 l posts dyal 24 sa3a (7tta 80), bach y3ref tkrar b ma3na 7tta ila tbeddlat siyagha. Khabar ta9riban b nafs l 3onwan kaytchedd bla Gemini. Ila khabar wsel bla nass w tsifet, melli kaywsel nass dyalo kaytsiftou ghir النسخة 1/2 (bla covers 3awtani).

Ila salaw kolchi models:
- Akhbar jdad ma kaytjajouch: kayb9aw f queue d judge w kayt3awdou f dowra jaya (7tta `MAX_AGE_HOURS`, 3 sa3at).
- Khabar li tsifet (card) w Gemini ma ktebch النسخة 1/2: kaydkhel f queue (`retry`), w kayt3awed wa7ed f kol dowra 7tta 12 sa3a. Mlli Gemini yjawb, النسخة 1, caption w covers kayttzado f nefs l card.

## Test local

```bash
pip install -r requirements.txt
DRY_RUN=1 NO_AI=1 python bot.py       # bla Telegram w bla Gemini
DRY_RUN=1 GEMINI_API_KEY=... python bot.py
```

**AI upscale:** ila tswira sghira (zoom > ×1 f portrait), bot kaykebbrha b Real-ESRGAN (`models/realesr-general-x4v3.onnx`, BSD-3) 3la CPU (~4-7 s). Tswira kat9ra bla mochkil, walakin copyright dyal tswira l asliya kayb9a.

**Tswira dyal chakhsiya:** ila l khabar 3la chakhsiya 3amma wa7da: 1) bot kayqelleb 3la tswira 7orra 9anouniya f Openverse (Wikimedia/Flickr: tsawer rasmiya d ra2asat, 7koumat, EU, w photographes CC), Gemini kaychouf 7tta 8 w kaykhtar a7san wa7da (bla caricature/rsoum); credit w licence (BY / BY-SA) kayjiw m3a tswira. 2) ila ma l9a walou: tswira HD (≥1000px) mn l web, ka référence (3endha copyright): Bing Images l owel, men ba3d DuckDuckGo (lib `ddgs`, mjani bla key, b smiya b l 3arbiya w men ba3d b l latiniya), w ila ma khdmouch (blocage) Google Images via https://serper.dev (secret `SERPER_API_KEY`, credits). Ila kayna tswira d chakhsiya, tswira ta3biriya ma kaytqelbch (bla call Gemini zayd). Serper 3ndo 2500 credit mra wa7da (machi kol chhar): bot kay7seb kol recherche w rapport 22:00 kayban ch7al b9a. Ila l compte deja sta3mel chi credits, 7ett `SERPER_CREDITS` (Variables) = ch7al b9a f serper.dev. **Alerts:** ila b9aw ≤ 100 credit (compteur) wla Serper rfed (credits salaw / key ghalet), bot kaysifet alert kbira f Telegram (w kaypinniha ila howa admin). Mlli salaw, bot kaykhdem b Bing/DuckDuckGo bo7dhom w kay3awed yjereb Serper kol 6 sa3at; ila beddelti `SERPER_API_KEY`, kay3ref dghya w compteur kaybda mn zero (b `SERPER_CREDITS`).

**Relay (MAP...):** MAP, Barlamane, Kech24, Goud kaybloquiw GitHub. Dir Cloudflare Worker fabor b `relay/worker.js`, w zid secrets `RELAY_URL` (lien d worker) w `RELAY_KEY` (nafs l mot de passe f worker w GitHub). Bla relay, had sites kaydouzo b Google News (3onwan bark, bla nass bla tswira). Ila site blocka 7tta l relay (403 Cloudflare "Just a moment" / 1003), bot kaywe9ef l relay dyalo 6 sa3at (f nafs run) w kaykhdem b Google News, bla ma y3awed kol d9i9a.

## Cover Instagram (automatique)

Kol card fiha covers **Post Instagram** wajdin (1080×1350, f Pack kayjiw document = quality kamla), msawbin b `cover.py`:

- **Forme A** (l 3adiya): tswira l fo9 katdoub f navy, titre kbir, catégorie gold. Tswira katkbar/katsghar 3la 7sab toul d titre.
- **Forme 3ajil**: forme A b pill "عاجل" 7amra w bar 7mer blast gold. Ila Gemini (judge) qal l khabar 3ajil (urgent) w score 9-10 (> `HIGH_SCORE`), kaydkhel blast A/D.
- **Forme match** (b7al Marca, bla titre): ghir ila l mawdou3 l asasi d l khabar howa natija d match sala (`match_result` = true; machi tasnif FIFA, tasri7at, ta7lil fih natija). Gemini kay3ti `match`: l fer9an, l ahdaf, li sjlou, l mosaba9a, smiya b l anglais): tswira 3amra, score kbir, chi3arat d l fer9an (TheSportsDB; ila ma tl9ach, kattketeb smiya kbira), li sjlou ta7t kol fari9. L fari9 l awel 3la limen. Kaydkhel blast A/D (w b l 7mer ila 3ajil).
- **Forme D**: tswira 3amra l post + cadre gold. Ghir ila tswira l asliya HD (bla AI, zoom ≤ 1.15) w machi 3rida bzaf (w/h ≤ 1.35) w titre ≤ 3 stoura.
- Jouj covers: wa7ed b tswira d l khabar (l asliya ila ≥ 600px — 1200×630 dyal sites kaydkhel), w wa7ed b tswira d l chakhsiya (rasmiya 7orra, sinon Google) wla, ila ma kaynach chakhsiya, b tswira ta3biriya 7orra (+ "صورة تعبيرية"). Ila ma kaynach wa7da mnhom, kaytsifet ghir l akhor.
- Titre = instagram_title (bla emoji), catégorie men Gemini.
- Alwan: navy `#0B1F4D` / `#16357A`, gold `#C9A227` / `#E6C65C`. Font Tajawal (OFL), logo `assets/logo.png`.
