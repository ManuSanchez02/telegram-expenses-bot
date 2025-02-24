import { Telegraf } from 'telegraf';
import { message } from 'telegraf/filters';
import dotenv from "dotenv";

dotenv.config();

const BOT_TOKEN = process.env.BOT_TOKEN;
const BOT_SERVICE_API_KEY = process.env.BOT_SERVICE_API_KEY;
if (!BOT_TOKEN) {
  throw new Error('BOT_TOKEN is required but was not provided');
} else if (!BOT_SERVICE_API_KEY) {
  throw new Error('BOT_SERVICE_API_KEY is required but was not provided');
}
// Replace with your bot token
const bot = new Telegraf(BOT_TOKEN);

// Start command
bot.start((ctx) => ctx.reply('Welcome! I am an expense tracker. Just type your expense and I will keep track of it.'));

// Help command
bot.help((ctx) => ctx.reply('Just type what you spent money on and how much money you spent, and I will keep track of it!'));


// Handle text messages
bot.on(message("text"), async (ctx) => {
  const res = await fetch('http://localhost:8000/parse', {
    method: 'POST',
    body: JSON.stringify({ text: ctx.message.text, telegram_id: ctx.message.from.id.toString() }),
    headers: {
      'Content-Type': 'application/json',
      'X-API-Key': BOT_SERVICE_API_KEY
    }

  });
  const body = await res.json();
  if (!res.ok) {
    if (body.detail?.error === 'incomplete_expense') {
      ctx.reply('Please provide both the expense and the amount spent.');
    } else if (body.detail?.error === 'user_not_found') {
      ctx.reply('You are not whitelisted to use this bot. Please contact the bot owner.');
    }
    return;
  }
  ctx.reply(body.message);
});

// Start bot
bot.launch();

process.once('SIGINT', () => bot.stop('SIGINT'))
process.once('SIGTERM', () => bot.stop('SIGTERM'))

console.log('Bot is running...');
