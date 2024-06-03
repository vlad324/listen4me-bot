# [@Listen4Me](https://t.me/l4me_bot) bot repository

The repository contains the code for the [@Listen4Me](https://t.me/l4me_bot) bot. The bot is designed to transcribe audio messages to text.

## Bot creation and local run

1. Create a new bot using [@BotFather](https://t.me/botfather). After creation process is finished, you will receive a token for your bot.
2. Generate a random string to use as a webhook secret.

```bash
openssl rand -hex 32
```

3. Clone the repository:

```bash
git clone https://github.com/vlad324/listen4me-bot
```

4. Install the necessary dependencies:

```bash
pip install -r requirements.txt
```

5. Create a `.env` file in the root of the project and specify the following environment variables in it:

```
OPEN_AI_API_KEY="your_open_ai_api_key"
TELEGRAM_BOT_TOKEN="your_telegram_bot_token"
TELEGRAM_WEBHOOK_SECRET="your_telegram_webhook_secret"
```

6. Run the bot:

```bash
fastapi run main.py --port 8000
```

The bot will be waiting for webhooks at `http://localhost:8000/l4me_bot/webhook`.

7. Using `ngrok`, expose the local server to the internet:

```bash
ngrok http 8000
```

8. Set the webhook for the bot:

```bash
curl -X POST --location "https://api.telegram.org/bot<BOT_TOKEN>/setWebhook" \
    -H "Content-Type: application/json" \
    -d '{
          "url": "<URL_PROVIDED_BY_NGROK>",
          "secret_token": "<RANDOM_GENERATED_STRING_FROM_STEP_3>"
        }'
```

## Deployment to [fly.io](https://fly.io)

1. Install the `flyctl` CLI tool by following the instructions on
   the [official website](https://fly.io/docs/getting-started/installing-flyctl/).
2. Sign in or sing up to the [fly.io](https://fly.io/docs/hands-on/sign-up-sign-in/) platform.
3. Launch a new app:

```bash
flyctl launch
```

4. Set the necessary secrets for the bot:

```bash
flyctl secrets set OPEN_AI_API_KEY=<your_open_ai_api_key> \
 TELEGRAM_BOT_TOKEN=<your_telegram_bot_token> \
 TELEGRAM_WEBHOOK_SECRET=<your_telegram_webhook_secret>
```

5. Deploy the bot to the platform:

```bash
fly deploy
```

6. Set the new webhook URL for the bot:

```bash
curl -X POST --location "https://api.telegram.org/bot<BOT_TOKEN>/setWebhook" \
    -H "Content-Type: application/json" \
    -d '{
          "url": "<URL_PROVIDED_BY_FLY_IO>",
          "secret_token": "<RANDOM_GENERATED_STRING_FROM_STEP_3>"
        }'
```