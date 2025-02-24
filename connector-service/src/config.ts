import dotenv from "dotenv";

dotenv.config();

const requiredEnvVars = ["BOT_TOKEN", "BOT_SERVICE_API_KEY", "BOT_SERVICE_URL"];
const missingVars = requiredEnvVars.filter((key) => !process.env[key]);

if (missingVars.length > 0) {
  throw new Error(
    `Missing required environment variables: ${missingVars.join(", ")}`,
  );
}

export const BOT_CONFIG = {
  TOKEN: process.env.BOT_TOKEN || "",
  API_KEY: process.env.BOT_SERVICE_API_KEY || "",
  SERVICE_URL: process.env.BOT_SERVICE_URL,
  WEBHOOK_DOMAIN: process.env.WEBHOOK_DOMAIN || null,
  PORT: parseInt(process.env.PORT || "3000", 10),
};
