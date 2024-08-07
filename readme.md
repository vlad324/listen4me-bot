# Listen4Me bot repository

The repository contains the code for the Listen4Me bot. The bot is available on Telegram and WhatsApp and designed to transcribe audio
messages to text.

Telegram bot: [@Listen4Me](https://t.me/l4me_bot)

WhatsApp bot: [@Listen4Me](https://wa.me/message/CZS3B3D7YNL3C1)

## Self-hosting options

The bot can be run on a local machine or deployed to a cloud platform.
There is an option to run the bot only for one of the platforms (Telegram or WhatsApp) or for both of them.

### Prerequisites

1. OpenAI API key. You can get it by signing up on the [Open AI website](https://platform.openai.com/signup).
2. Telegram bot token. You can create a new bot using [@BotFather](https://t.me/botfather). If you plan to run the bot only for WhatsApp,
   you can omit this step.
3. WhatsApp API key and phone number id. You can get it by creating WhatsApp app
   on [Meta for Developers](https://developers.facebook.com/apps) platform. If you plan to run the bot only for Telegram, you can omit this
   step.
4. Two random string. First one to use as a webhook secret for Telegram, and the second one for verify token for WhatsApp.

There are several ways to run the bot locally:
<details>
<summary><b>Local run with ngrok endpoint</b></summary>

1. Clone the repository:

```bash
git clone https://github.com/vlad324/listen4me-bot
```

2. Install the necessary dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root of the project and specify the following environment variables in it:

```
OPEN_AI_API_KEY=your_open_ai_api_key

TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_WEBHOOK_SECRET=first_random_string_generated_in_prerequisites_section

WA_API_KEY=api_key_of_your_whatsapp_app
WA_PHONE_NUMBER_ID=phone_number_id_of_your_whatsapp_app
WA_VERIFY_TOKEN=second_random_string_generated_in_prerequisites_section
```

If you plan to run the bot only for Telegram or WhatsApp, you can omit the corresponding variables. `OPEN_AI_API_KEY` is required for both
platforms.

4. Run the bot:

```bash
fastapi run app/main.py --port 8000
```

The bot will be waiting for webhooks at `http://localhost:8000/telegram/l4me_bot/webhook` for Telegram
and `http://localhost:8000/whatsapp/l4me_bot/webhook` for WhatsApp.

5. Using `ngrok`, expose your local server to the internet:

```bash
ngrok http 8000
```

6. Set the webhook for Telegram the bot:

```bash
curl -X POST --location "https://api.telegram.org/bot<BOT_TOKEN>/setWebhook" \
    -H "Content-Type: application/json" \
    -d '{
          "url": "<url_provided_by_ngrok>/telegram/l4me_bot/webhook",
          "secret_token": "<first_random_string_generated_in_prerequisites_section>"
        }'
```

7. Use Meta for Developers platform to set the webhook for WhatsApp bot. URL should be `<url_provided_by_ngrok>/whatsapp/l4me_bot/webhook`
   and verify token should be `<second_random_string_generated_in_prerequisites_section>`.

</details>

<details>
<summary><b>Local run with Docker and ngrok endpoint</b></summary>

1. Clone the repository:

```bash
git clone https://github.com/vlad324/listen4me-bot
```

2. Build the Docker image:

```bash
docker build -t listen4me-bot .
```

3. Create a `.env` file in the root of the project and specify the following environment variables in it:

```
OPEN_AI_API_KEY=your_open_ai_api_key

TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_WEBHOOK_SECRET=first_random_string_generated_in_prerequisites_section

WA_API_KEY=api_key_of_your_whatsapp_app
WA_PHONE_NUMBER_ID=phone_number_id_of_your_whatsapp_app
WA_VERIFY_TOKEN=second_random_string_generated_in_prerequisites_section
```

If you plan to run the bot only for Telegram or WhatsApp, you can omit the corresponding variables. `OPEN_AI_API_KEY` is required for both
platforms.

4. Run the Docker container:

```bash
docker run --env-file .env -p 8080:8080 listen4me-bot
```

5. Using `ngrok`, expose your local server to the internet:

```bash
ngrok http 8080
```

6. Set the webhook for Telegram the bot:

```bash
curl -X POST --location "https://api.telegram.org/bot<BOT_TOKEN>/setWebhook" \
    -H "Content-Type: application/json" \
    -d '{
          "url": "<url_provided_by_ngrok>/telegram/l4me_bot/webhook",
          "secret_token": "<first_random_string_generated_in_prerequisites_section>"
        }'
```

7. Use Meta for Developers platform to set the webhook for WhatsApp bot. URL should be `<url_provided_by_ngrok>/whatsapp/l4me_bot/webhook`
   and verify token should be `<second_random_string_generated_in_prerequisites_section>`.

</details>

### Deployment to [fly.io](https://fly.io)

The bot can be deployed to the [fly.io](https://fly.io) platform. The platform provides a free tier for small applications and could be a
good option to host your own instance of the bot.

1. Install the `flyctl` CLI tool by following the instructions on
   the [official website](https://fly.io/docs/getting-started/installing-flyctl/).
2. Sign in or sing up to the [fly.io](https://fly.io/docs/hands-on/sign-up-sign-in/) platform.
3. Launch a new app:

```bash
flyctl launch
```

4. Set the necessary secrets for the bot:

```bash
flyctl secrets set OPEN_AI_API_KEY=<your_open_ai_api_key>
```

Telegram related secrets:

```bash
flyctl secrets set TELEGRAM_BOT_TOKEN=<your_telegram_bot_token> \
 TELEGRAM_WEBHOOK_SECRET=<first_random_string_generated_in_prerequisites_section>
```

WhatsApp related secrets:

```bash
flyctl secrets set WA_API_KEY=<api_key_of_your_whatsapp_app> \
 WA_PHONE_NUMBER_ID=<phone_number_id_of_your_whatsapp_app> \
 WA_VERIFY_TOKEN=<second_random_string_generated_in_prerequisites_section>
```

If you plan to run the bot only for Telegram or WhatsApp, you can omit the corresponding secrets. `OPEN_AI_API_KEY` is required for both

5. Deploy the bot to the platform:

```bash
fly deploy
```

6. Set the new webhook URL for Telegram bot:

```bash
curl -X POST --location "https://api.telegram.org/bot<BOT_TOKEN>/setWebhook" \
    -H "Content-Type: application/json" \
    -d '{
          "url": "<url_provided_by_fly_io>/telegram/l4me_bot/webhook",
          "secret_token": "<first_random_string_generated_in_prerequisites_section>"
        }'
```

7. Use Meta for Developers platform to set the webhook for WhatsApp bot. URL should be `<url_provided_by_fly_io>/whatsapp/l4me_bot/webhook`
   and verify token should be `<second_random_string_generated_in_prerequisites_section>`.

## Restricting access to your Telegram bot

To limit access to your version of the Telegram bot, you'll need to know your Telegram id or the Telegram ids of users you want to grant
access to.
Here's how to obtain this information:

1. Start a conversation with [@GetIDs Bot](https://t.me/getidsbot) on Telegram.
2. The bot will send you a message containing your Telegram id. Copy this id.

Once you have the necessary ids, follow these steps to restrict access:

### For local deployment:

Add the following line to your `.env` file:

```
TELEGRAM_ALLOWED_USER_IDS=<id_1,id_2,...>
```

Replace `<id_1,id_2,...>` with a single Telegram ID or a comma-separated list of allowed Telegram IDs. For example:

- For a single user: `TELEGRAM_ALLOWED_USER_IDS=123456789`
- For multiple users: `TELEGRAM_ALLOWED_USER_IDS=123456789,987654321`

### For fly.io deployment:

Execute the following command:

```bash
flyctl secrets set TELEGRAM_ALLOWED_USER_IDS=<id_1,id_2,...>
```

Replace `<id_1,id_2,...>` with the comma-separated list of Telegram IDs for users you want to allow access to your bot.

By setting this environment variable, you'll ensure that only specified users can interact with your Telegram bot.