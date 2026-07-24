# jan_clode_van_dam

**Telegram Bot powered by Anthropic Claude AI** – fetches Tech Forum discussions and generates SEO Schema, Feed digests, and Forum analyses.

---

## Features

| Command | Description |
|---|---|
| `/start` | Introduction and usage guide |
| `/help` | List all available commands |
| `/schema <url>` | Generate JSON-LD SEO Schema markup for any URL |
| `/feed <url>` | Fetch and summarise an RSS/Atom tech feed |
| `/forums <topic>` | Search and analyse tech forum discussions (Stack Overflow, Hacker News) |

---

## Prerequisites

- Python 3.11+
- A [Telegram Bot token](https://core.telegram.org/bots/tutorial) from @BotFather
- An [Anthropic API key](https://console.anthropic.com/)

---

## Setup

```bash
# 1. Clone the repo
git clone https://github.com/Artsrun/jan_clode_van_dam.git
cd jan_clode_van_dam

# 2. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment variables
cp .env.example .env
# Edit .env and fill in TELEGRAM_BOT_TOKEN and ANTHROPIC_API_KEY

# 5. Run the bot
python bot.py
```

---

## Project Structure

```
jan_clode_van_dam/
├── bot.py                  # Main entry point
├── config.py               # Centralised configuration (reads .env)
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variable template
├── handlers/
│   ├── start.py            # /start and /help handlers
│   ├── schema.py           # /schema handler – SEO JSON-LD generation
│   ├── feed.py             # /feed handler – RSS/Atom feed digest
│   └── forums.py           # /forums handler – tech forum analysis
└── utils/
    ├── claude_client.py    # Anthropic Claude AI wrapper
    └── fetcher.py          # RSS feed & web page fetching utilities
```

---

## Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `TELEGRAM_BOT_TOKEN` | ✅ | – | Bot token from @BotFather |
| `ANTHROPIC_API_KEY` | ✅ | – | Anthropic API key |
| `CLAUDE_MODEL` | ❌ | `claude-3-5-sonnet-20241022` | Claude model to use |
| `CLAUDE_MAX_TOKENS` | ❌ | `2048` | Max tokens per Claude response |
| `REQUEST_TIMEOUT` | ❌ | `15` | HTTP request timeout (seconds) |
| `LOG_LEVEL` | ❌ | `INFO` | Logging verbosity |

---

## License

[MIT](LICENSE)
