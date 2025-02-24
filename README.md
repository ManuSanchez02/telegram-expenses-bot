# Expense Tracker

## Description

This repository contains the code for an expense tracking telegram bot. The bot is built using `telegraf` for the connection layer, and `FastAPI`, `SQLAlchemy` and `langchain` for the parsing and persistence layer.

## Installation

To install the bot, you need to have the following dependencies installed:

- `uv 0.6.2` or greater.
- `Node.js LTS 22.14.0` or greater.

After installing these, you have to `cd` into the `bot-service` directory and run the following commands:

```bash
uv sync
```

After that, you should `cd` into the `connector-service` directory and run the following commands:

```bash
npm install
```

Once the dependencies are installed, you can go ahead and run the services.

## Environment Variables

Before going on any further, you need to create a `.env` file in the `bot-service` and `connector-service` directories. In order to do so, you can copy the `.env.example` file in the respective directories and rename it to `.env`. THen you can fill in the values for the environment variables.

### Bot Service

The following environment variables are required for the bot service:

```env
AI21_API_KEY=<YOUR_API_KEY> # The API key for the AI21 API.
POSTGRES_USER=<YOUR_POSTGRES_USER>
POSTGRES_PASSWORD=<YOUR_POSTGRES_PASSWORD>
POSTGRES_DB=<YOUR_POSTGRES_DB>
POSTGRES_HOST=<YOUR_POSTGRES_HOST>
LOG_LEVEL=INFO
```

### Connector Service

The following environment variables are required for the connector service:

```env
BOT_TOKEN=<YOUR_BOT_TOKEN> # The token for the telegram bot, obtained from the BotFather.
BOT_SERVICE_URL=<YOUR_BOT_SERVICE_URL> # The URL for the bot service.
BOT_SERVICE_API_KEY=<YOUR_BOT_SERVICE_API_KEY> # The API key for the bot service.
WEBHOOK_DOMAIN=<YOUR_WEBHOOK_DOMAIN> # The domain for the webhook.
WEBHOOK_PORT=<YOUR_WEBHOOK_PORT> # The port for the webhook. Defaults to 3000.
```

The `BOT_SERVICE_API_KEY` is a secret key that is used to authenticate requests from the connector service to the bot service. It is generated by the bot service the first time it is run, and should be copied to the `.env` file in the connector service.

## Running the services

To run the bot service, you have to `cd` into the `bot-service` directory and run the following command:

```bash
uv run fastapi run
```

Once the bot service is running, you can start the connector service by `cd`ing into the `connector-service` directory and running the following commands:

```bash
npm run build && npm run start
```

After running these commands, the bot should be up and able to reply to messages.

## Usage

In order to use the bot, you can directly message it on telegram. However, keep in mind that if you are not whitelisted, the bot will not respond to your messages.
