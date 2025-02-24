import { Telegraf } from "telegraf";
import { message } from "telegraf/filters";
import crypto from "crypto";
import { BOT_CONFIG } from "./config.js";
import { processExpense } from "./expenseHandler.js";
import logger from "./logger.js";

const bot = new Telegraf(BOT_CONFIG.TOKEN);

// Start command
bot.start((ctx) =>
  ctx.reply(
    "Welcome! I am an expense tracker. Just type your expense and I will keep track of it."
  )
);

// Help command
bot.help((ctx) =>
  ctx.reply(
    "Just type what you spent money on and how much money you spent, and I will keep track of it!"
  )
);

// Handle text messages
bot.on(message("text"), async (ctx) => {
  logger.info(
    `Received message from ${ctx.message.from.id}: ${ctx.message.text}`
  );
  const replyMessage = await processExpense(
    ctx.message.text,
    ctx.message.from.id.toString()
  );
  if (replyMessage) ctx.reply(replyMessage);
});

const startBot = async () => {
  try {
    if (BOT_CONFIG.WEBHOOK_DOMAIN) {
      logger.info("Launching bot in webhook mode...");
      bot.launch(
        {
          webhook: {
            domain: BOT_CONFIG.WEBHOOK_DOMAIN,
            port: BOT_CONFIG.WEBHOOK_PORT,
            secretToken: crypto.randomBytes(64).toString("hex"),
          },
        },
        () => logger.info("Bot is running...")
      );
    } else {
      logger.info("Launching bot in polling mode...");
      bot.launch(() => logger.info("Bot is running..."));
    }
  } catch (error: any) {
    logger.error(`Error launching bot: ${error.message}`);
  }
};

// Graceful shutdown
process.once("SIGINT", () => bot.stop("SIGINT"));
process.once("SIGTERM", () => bot.stop("SIGTERM"));

// Start bot
startBot();
