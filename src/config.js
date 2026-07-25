import 'dotenv/config';

function required(name) {
  const value = process.env[name];
  if (!value) {
    throw new Error(`Missing required environment variable: ${name}`);
  }
  return value;
}

export const config = {
  telegramToken: required('TELEGRAM_BOT_TOKEN'),
  anthropicKey: required('ANTHROPIC_API_KEY'),
  model: process.env.CLAUDE_MODEL || 'claude-3-5-sonnet-20241022',
  systemPrompt:
    process.env.SYSTEM_PROMPT ||
    'You are Jan Clode Van Dam — a slightly eccentric, precise, and helpful AI assistant living inside a Telegram bot. You think in elegant systems, notice hidden patterns, and never over-explain.',
  allowedUserIds: (process.env.ALLOWED_USER_IDS || '')
    .split(',')
    .map((id) => id.trim())
    .filter(Boolean)
    .map(Number),
};
