# News bot (Telegram + Gemini)

Kayraqeb ~24 source dyal l akhbar f l Maghrib kol 60 tanya. Kol khabar jdid kaywselk f Telegram f 3 messages:

1. **Alerte** (sa3a ghir tban): source, sa3a, 3onwan, lien.
2. **النسخة 1**: nafs l khabar b siyagha jdida (bla zyada, bla na9s, arqam/asma/iqtibasat kif ma homa).
3. **النسخة 2**: version qsira l Instagram + hashtags.

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
6. **Tkhdem 24/24**: f nafs l page → tab *Variables* → `NEWS_BOT_ENABLED` = `true`.

Variables ikhtiyariyin: `GEMINI_MODELS`, `POLL_SECONDS`, `RUN_MINUTES`.

## Mohim

- Repo public: d9aye9 GitHub Actions bla 7did, free. L keys f Secrets, ma kayban walou.
- GitHub kaytfi l workflows `schedule` ila ma kan 7ta commit 60 youm. Dir commit sghir mra f chhar (mthal bdel `sources.json`).

## Limites Gemini free

Free tier 3ndo limite d requests f l youm (kaytbedel 3la 7sab model). Ila t9ada `gemini-2.5-flash`, bot kaydouz l `gemini-2.5-flash-lite`. Ila t9adaw b jouj, kaywselk ghir l alerte + "Gemini ma jawebsh". L 7ul: 7bes sources li ma kat7tajhoumch.

## Test local

```bash
pip install -r requirements.txt
DRY_RUN=1 NO_AI=1 python bot.py       # bla Telegram w bla Gemini
DRY_RUN=1 GEMINI_API_KEY=... python bot.py
```
