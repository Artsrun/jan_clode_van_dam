# jan_clode_van_dam

**Telegram Bot + Claude API**  
Jean-Claude Van Damme energy, Claude brain, JavaScript skeleton.

> Always bet on JavaScript. Always keep the system elegant.

## What this is

A clean, production-ready starting point for a Telegram bot that talks to Anthropic's Claude.

- **Telegraf** for the Telegram layer
- **@anthropic-ai/sdk** for Claude
- Minimal, explicit structure
- Env-based config, no secrets in repo
- Ready for further handlers, memory, tools, or multi-agent experiments

## Quick start

```bash
# 1. Clone
git clone https://github.com/Artsrun/jan_clode_van_dam.git
cd jan_clode_van_dam

# 2. Install
npm install

# 3. Configure
cp .env.example .env
# edit .env → put your TELEGRAM_BOT_TOKEN + ANTHROPIC_API_KEY

# 4. Run
npm start
# or with auto-reload:
npm run dev
```

## Project layout

```
.
├── .env.example          # template — copy to .env
├── .gitignore
├── LICENSE               # GPL-3.0
├── package.json
├── README.md
└── src/
    ├── index.js           # entry point
    ├── config.js          # loads & validates env
    ├── claude.js          # thin Anthropic client wrapper
    └── bot.js             # Telegraf instance + handlers
```

## Environment variables

| Variable | Required | Description |
|----------|----------|-------------|
| `TELEGRAM_BOT_TOKEN` | yes | From @BotFather |
| `ANTHROPIC_API_KEY` | yes | From Anthropic console |
| `ALLOWED_USER_IDS` | no | Comma-separated Telegram user IDs (whitelist) |
| `CLAUDE_MODEL` | no | Defaults to `claude-3-5-sonnet-20241022` |
| `SYSTEM_PROMPT` | no | Personality / system instruction |

## Next moves (suggested)

- Add conversation memory (per-chat Map or Redis)
- Tool use / function calling for Claude
- Rate limiting + abuse protection
- Structured logging
- Deploy (Railway / Fly.io / your own VPS)

## License

GPL-3.0 — see [LICENSE](LICENSE)
