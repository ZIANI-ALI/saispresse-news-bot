# News bot (Telegram + Gemini)

Kayraqeb ~24 source dyal l akhbar f l Maghrib kol 60 tanya. Kol khabar jdid kaywselk f Telegram f 3 messages:

1. **Alerte** (sa3a ghir tban): source, sa3a, 3onwan, lien.
2. **النسخة 1**: nafs l khabar b siyagha jdida (bla zyada, bla na9s, arqam/asma/iqtibasat kif ma homa).
3. **النسخة 2**: version qsira l Instagram + hashtags.

**Ghir l mohim:** Gemini kay3ti l kol khabar note d ahamiya mn 10. Kolchi li 3ndo `MIN_SCORE` (7) wla ktar kaytsifet bla 7add (bla limite f sa3a). `HIGH_SCORE` (8): ghir l 9-10 (> 8) kaykounou 3ajil. Tqder tbdel had l ar9am men Variables.

**Akhbar dawliya:** sources b `"intl": true` (سكاي نيوز عربية، بي بي سي عربي; الجزيرة w فرانس 24 m7bousin: feed bati2). Khabar dawli kaytsifet b7al l akhrin: score >= `MIN_SCORE` (7).

**Kora:** sources رياضة (هسبورت، سكاي نيوز عربية رياضة، ماركا ريال مدريد/برشلونة، آس، موندو ديبورتيفو برشلونة/ريال مدريد). Gemini (judge) kay3ref l khabar dyal kora (`football`) w kay3tih score b slom khas: 8 = natija d l mountakhab, ay match d l Botola, l fera9 l maghribiya f Afri9ya, l mountakhabat l kbar, transfer d la3ib maghribi wla star, akhbar kbar d Real/Barça; 7 = akhbar Real/Barça dyal Marca, akhbar l fera9 l maghribiya, la3ibin maghariba f Oropa. Kora kattsifet mn 7+ 7tta ila kant dawliya.

**Khabar bla nass** (Google News / site kayblocki): ma kaytsiftsh; bot kaytsna 7tta source okhra tjib nafs l khabar b l article, w 3ad kaysifeto kamel (cover + النسخة 1/2). Ghir ila score 9-10: kaytsifet daba b cover men l 3onwan bark (bla versions), w mnin ywsel l article men source okhra kaytsifet tani kamel ("📄 النص الكامل وصل").

**Kol khabar:** tswira + 3onwan asli (+ note) → النسخة 1 → Instagram (3onwan viral + 2-3 fiqrat). Kol khabar kaybda b khatt fasel w ra9mo f nhar.

**Tsawer 7orra (Pexels / Pixabay / Openverse):** Gemini kay3ti 3 recherches (mn d9i9a l 3amma, b7al `bone in red dirt | skull buried soil | crime scene tape`); l kol wa7da kayjereb Pexels/Pixabay, w ila walou Openverse (majjani bla key: Flickr, Wikimedia; ghir CC0/PDM/BY/BY-SA). Tsawer d Openverse kayjiw b credit w licence; BY-SA kat3ni cover khasso nafs l licence. zid secret `PIXABAY_API_KEY` (majjani, l key kayban f https://pixabay.com/api/docs/ men b3d login) wla `PEXELS_API_KEY` (https://www.pexels.com/api/, daba mwe99fin keys jdad). Ila kaynin b jouj, Pexels lowel w Pixabay ila ma l9a walou. Kol khabar kayjih tswira HD bla copyright f 3 formats (portrait 4:5, carré 1:1, site 16:9), mkhtara 3la 7sab l mawdou3. Tswira d l source katb9a référence bark.

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

Variables ikhtiyariyin: `MIN_SCORE`, `HIGH_SCORE`, `GEMINI_MODELS`, `POLL_SECONDS`, `RUN_MINUTES`.

## Mohim

- Repo public: d9aye9 GitHub Actions bla 7did, free. L keys f Secrets, ma kayban walou.
- GitHub kaytfi l workflows `schedule` ila ma kan 7ta commit 60 youm. Dir commit sghir mra f chhar (mthal bdel `sources.json`).

## Limites Gemini free

Free tier 3ndo limite d requests f l youm, w kol model 3ndo quota dyalo. Bot kaykhtar automatiquement a7dath flash, a7dath flash-lite w flash tani; model li rja3 429 kayt7bes (1 min ila quota d d9i9a, 1 sa3a ila quota d nhar) w kaydouz l li mor.

Ila salaw kolchi models:
- Akhbar jdad ma kaytjajouch: kayb9aw f tsna w kayt3awdou f dowra jaya (7tta `MAX_AGE_HOURS`, 3 sa3at).
- Khabar li tsifet (alerte) w Gemini ma ktebch النسخة 1/2: kaydkhel f queue (`retry`), w kayt3awed wa7ed f kol dowra 7tta 12 sa3a. Versions + covers kaywslo reply 3la l alerte.

## Test local

```bash
pip install -r requirements.txt
DRY_RUN=1 NO_AI=1 python bot.py       # bla Telegram w bla Gemini
DRY_RUN=1 GEMINI_API_KEY=... python bot.py
```

**AI upscale:** ila tswira sghira (zoom > ×1 f portrait), bot kaykebbrha b Real-ESRGAN (`models/realesr-general-x4v3.onnx`, BSD-3) 3la CPU (~4-7 s). Tswira kat9ra bla mochkil, walakin copyright dyal tswira l asliya kayb9a.

**Tswira dyal chakhsiya (Google):** ila l khabar 3la chakhs wa7ed w tswira d l source sghira, bot kayqelleb f Google Images (via https://serper.dev, secret `SERPER_API_KEY`) 3la tswira HD (≥1000px) w kaysifetha ka référence (3endha copyright). Serper 3ndo 2500 credit mra wa7da (machi kol chhar): bot kay7seb kol recherche w rapport 22:00 kayban ch7al b9a. Ila l compte deja sta3mel chi credits, 7ett `SERPER_CREDITS` (Variables) = ch7al b9a f serper.dev.

**Relay (MAP...):** MAP, Barlamane, Kech24, Goud kaybloquiw GitHub. Dir Cloudflare Worker fabor b `relay/worker.js`, w zid secrets `RELAY_URL` (lien d worker) w `RELAY_KEY` (nafs l mot de passe f worker w GitHub). Bla relay, had sites kaydouzo b Google News (3onwan bark, bla nass bla tswira).

## Cover Instagram (automatique)

Kol khbar kaywsel m3ah **Post Instagram** wajed (1080×1350, document = quality kamla), msawb b `cover.py`:

- **Forme A** (l 3adiya): tswira l fo9 katdoub f navy, titre kbir, catégorie gold. Tswira katkbar/katsghar 3la 7sab toul d titre.
- **Forme 3ajil**: forme A b pill "عاجل" 7amra w bar 7mer blast gold. Ila Gemini (judge) qal l khabar 3ajil (urgent) w score 9-10 (> `HIGH_SCORE`), kaydkhel blast A/D.
- **Forme match** (b7al Marca, bla titre): ghir ila l mawdou3 l asasi d l khabar howa natija d match sala (`match_result` = true; machi tasnif FIFA, tasri7at, ta7lil fih natija). Gemini kay3ti `match`: l fer9an, l ahdaf, li sjlou, l mosaba9a, smiya b l anglais): tswira 3amra, score kbir, chi3arat d l fer9an (TheSportsDB; ila ma tl9ach, kattketeb smiya kbira), li sjlou ta7t kol fari9. L fari9 l awel 3la limen. Kaydkhel blast A/D (w b l 7mer ila 3ajil).
- **Forme D**: tswira 3amra l post + cadre gold. Ghir ila tswira l asliya HD (bla AI, zoom ≤ 1.15) w machi 3rida bzaf (w/h ≤ 1.35) w titre ≤ 3 stoura.
- Jouj covers: wa7ed b tswira d l khabar (l asliya ila ≥ 600px — 1200×630 dyal sites kaydkhel — sinon Google chakhsiya), w wa7ed b tswira 7orra (+ "صورة تعبيرية"). Ila ma kaynach wa7da mnhom, kaytsifet ghir l akhor.
- Titre = instagram_title (bla emoji), catégorie men Gemini.
- Alwan: navy `#0B1F4D` / `#16357A`, gold `#C9A227` / `#E6C65C`. Font Tajawal (OFL), logo `assets/logo.png`.
