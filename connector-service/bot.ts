import { Telegraf } from 'telegraf';
import { message } from 'telegraf/filters';
import dotenv from "dotenv";
import crypto from "crypto";
import express from 'express';

dotenv.config();

const BOT_TOKEN = process.env.BOT_TOKEN;
const BOT_SERVICE_API_KEY = process.env.BOT_SERVICE_API_KEY;
const BOT_SERVICE_URL = process.env.BOT_SERVICE_URL;
if (!BOT_TOKEN) {
  throw new Error('BOT_TOKEN is required but was not provided');
} else if (!BOT_SERVICE_API_KEY) {
  throw new Error('BOT_SERVICE_API_KEY is required but was not provided');
} else if (!BOT_SERVICE_URL) {
  throw new Error('BOT_SERVICE_URL is required but was not provided');
}

const app = express();
app.use(express.json());

// Telegram will send updates to this route
app.post(`/bot${BOT_TOKEN}`, (req, res) => {
  console.log('Received update:', req.body);
  bot.handleUpdate(req.body);
  res.sendStatus(200);
});

app.listen(process.env.PORT || 3000, () => {
  console.log(`Connector service is running on port ${process.env.PORT || 3000}`);
});

// Replace with your bot token
const bot = new Telegraf(BOT_TOKEN);

// Start command
bot.start((ctx) => ctx.reply('Welcome! I am an expense tracker. Just type your expense and I will keep track of it.'));

// Help command
bot.help((ctx) => ctx.reply('Just type what you spent money on and how much money you spent, and I will keep track of it!'));


// Handle text messages
bot.on(message("text"), async (ctx) => {
  console.log('Received message:', ctx.message.text);
  try {
    const res = await fetch(`${BOT_SERVICE_URL}/parse`, {
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
  }
  catch (error) {
    console.error('Error:', error);
  }
});

if (process.env.WEBHOOK_DOMAIN) {
  bot.launch({
    webhook: {
      domain: process.env.WEBHOOK_DOMAIN,
      port: parseInt(process.env.PORT || '443'),
      secretToken: crypto.randomBytes(64).toString("hex"),
    }
  });

} else {
  bot.launch();
}


// Start bot

process.once('SIGINT', () => bot.stop('SIGINT'))
process.once('SIGTERM', () => bot.stop('SIGTERM'))

console.log('Bot is running...');
