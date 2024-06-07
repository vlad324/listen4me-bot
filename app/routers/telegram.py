import os
from typing import Any, Annotated

import requests
from dotenv import load_dotenv
from fastapi import BackgroundTasks, Body, Header, HTTPException, APIRouter

from ..dependecies import get_console_logger, transcribe_audio

load_dotenv()

router = APIRouter(prefix="/telegram", tags=["telegram"])

logger = get_console_logger("transcribe-bot-telegram")

token = os.getenv("TELEGRAM_BOT_TOKEN")
webhook_secret = os.getenv("TELEGRAM_WEBHOOK_SECRET")


def send_message(chat_id: str, text: str, reply_to_message_id: str | None = None) -> None:
    if reply_to_message_id is None:
        data = {
            "chat_id": chat_id,
            "text": text
        }
    else:
        data = {
            "chat_id": chat_id,
            "text": text,
            "reply_parameters": {
                "message_id": reply_to_message_id
            }
        }
    response = requests.post(f"https://api.telegram.org/bot{token}/sendMessage", json=data)
    response.raise_for_status()


def load_file_content(url):
    r = requests.get(url)
    r.raise_for_status()
    return r.content


class AudioProcessingTask:
    def __init__(self, chat_id: str, message_id: str, file_id: str):
        self.chat_id = chat_id
        self.message_id = message_id
        self.file_id = file_id


# TODO: make this more robust, handle errors and retries
def process_audio(task: AudioProcessingTask) -> None:
    response = requests.get(f"https://api.telegram.org/bot{token}/getFile?file_id={task.file_id}")
    response.raise_for_status()

    file_path = response.json()["result"]["file_path"]
    file_content = load_file_content(f"https://api.telegram.org/file/bot{token}/{file_path}")

    transcription = transcribe_audio(file_path.split("/")[-1], file_content)
    send_message(task.chat_id, transcription, task.message_id)


@router.post("/l4me_bot/webhook")
async def handle_webhook(background_tasks: BackgroundTasks,
                         x_telegram_bot_api_secret_token: Annotated[str | None, Header()] = None,
                         payload: Any = Body(None)):
    if x_telegram_bot_api_secret_token != webhook_secret:
        logger.error("Invalid secret token provided: %s", x_telegram_bot_api_secret_token)
        raise HTTPException(status_code=400, detail="Invalid secret token provided")

    message = payload["message"]
    chat_id = str(message["chat"]["id"])
    message_id = str(message["message_id"])
    if message.get("voice"):
        voice = message["voice"]
        task = AudioProcessingTask(chat_id, message_id, voice["file_id"])
        background_tasks.add_task(process_audio, task)
    elif message.get("video_note"):
        video_note = message["video_note"]
        task = AudioProcessingTask(chat_id, message_id, video_note["file_id"])
        background_tasks.add_task(process_audio, task)
        pass
    elif message.get("text") == "/start":
        send_message(chat_id, "Hello there! 👋 Send or forward me a voice message and I will transcribe it for you.")
    else:
        send_message(chat_id, "At the moment, I can only process and understand audio messages. 🙈", message_id)

    return {}
