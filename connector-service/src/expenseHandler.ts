import { BOT_CONFIG } from "./config.js";
import logger from "./logger.js";

export const processExpense = async (text: string, telegramId: string) => {
  try {
    const response = await fetch(`${BOT_CONFIG.SERVICE_URL}/parse`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-API-Key": BOT_CONFIG.API_KEY,
      },
      body: JSON.stringify({ text, telegram_id: telegramId.toString() }),
    });

    if (!response.ok) {
      const errorBody = await response.json();
      logger.error(
        `API Error ${response.status}: ${JSON.stringify(errorBody)}`
      );

      if (errorBody?.detail?.error === "incomplete_expense") {
        return "Please provide both the expense and the amount spent.";
      } else if (errorBody?.detail?.error === "user_not_found") {
        return "You are not whitelisted to use this bot. Please contact the bot owner.";
      } else if (errorBody?.detail?.error === "invalid_expense") {
        return; // Return nothing if the message is not expense related
      } else {
        return "An error occurred while processing your request. Please try again later.";
      }
    }

    const responseBody = await response.json();
    return responseBody.message;
  } catch (error: any) {
    logger.error(`Unexpected Error: ${error.message}`);
    return "An unexpected error occurred. Please try again later.";
  }
};
