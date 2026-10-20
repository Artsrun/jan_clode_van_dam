import { Telegraf } from 'telegraf';
import { config } from './config.js';
import { askClaude } from './claude.js';

export function createBot() {
  const bot = new Telegraf(config.telegramToken);

  // Simple whitelist middleware (optional)
  bot.use(async (ctx, next) => {
    if (config.allowedUserIds.length === 0) {
      return next();
    }
    const userId = ctx.from?.id;
    if (!userId || !config.allowedUserIds.includes(userId)) {
      await ctx.reply('Access denied. This bot is private.');
      return;
    }
    return next();
  });

  bot.start(async (ctx) => {
    await ctx.reply(
      'Jan Clode Van Dam online.\n\nSend me a message and I will think with Claude.',
    );
  });

  bot.help(async (ctx) => {
    await ctx.reply(
      'Just talk to me. I route your words through Claude and reply with the result.\n\nNo special commands yet — keep it simple.',
    );
  });

  // Main message handler
  bot.on('text', async (ctx) => {
    const text = ctx.message.text;

    // Ignore empty or very short noise
    if (!text || text.trim().length < 1) return;

    try {
      // Show typing indicator while Claude thinks
      await ctx.sendChatAction('typing');

      const reply = await askClaude(text);
      await ctx.reply(reply);
    } catch (err) {
      console.error('[bot] Claude error:', err.message);
      await ctx.reply('Something went sideways while talking to Claude. Check the logs.');
    }
  });

  // Catch-all for non-text (photos, stickers, etc.)
  bot.on('message', async (ctx) => {
    if (ctx.message.text) return; // already handled
    await ctx.reply('I only speak in text for now. Send words.');
  });

  return bot;
}
