import { createBot } from './bot.js';
import { config } from './config.js';

console.log('Starting Jan Clode Van Dam...');
console.log(`Model: ${config.model}`);
console.log(
  `Whitelist: ${config.allowedUserIds.length ? config.allowedUserIds.join(', ') : 'open (anyone)'}`,
);

const bot = createBot();

bot.launch().then(() => {
  console.log('Bot is running. Ctrl+C to stop.');
});

// Graceful shutdown
process.once('SIGINT', () => bot.stop('SIGINT'));
process.once('SIGTERM', () => bot.stop('SIGTERM'));
