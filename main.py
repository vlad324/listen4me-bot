import logging
import os
import sys
from typing import Any

import requests
from fastapi import FastAPI, BackgroundTasks, Body
from openai import OpenAI

logger = logging.getLogger("transcribe-bot")
logger.setLevel(logging.DEBUG)

console_log_handler = logging.StreamHandler(sys.stdout)
console_log_handler.setFormatter(logging.Formatter("%(asctime)s.%(msecs)03.0f [%(threadName)s] %(levelname)s %(module)s - %(message)s",
                                                   "%Y-%m-%d %H:%M:%S"))
logger.addHandler(console_log_handler)

app = FastAPI(docs_url=None, redoc_url=None)

client = OpenAI(api_key=os.getenv("OPEN_AI_API_KEY"))
token = os.getenv("TELEGRAM_BOT_TOKEN")


def send_message(chat_id: str, text: str, replay_to_message_id: str | None = None) -> None:
    if replay_to_message_id is None:
        data = {
            "chat_id": chat_id,
            "text": text
        }
    else:
        data = {
            "chat_id": chat_id,
            "text": text,
            "reply_parameters": {
                "message_id": replay_to_message_id
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

    transcription = client.audio.transcriptions.create(model="whisper-1", file=(file_path.split("/")[-1], file_content))
    send_message(task.chat_id, transcription.text, task.message_id)


@app.post("/l4me_bot/webhook")
async def handle_webhook(background_tasks: BackgroundTasks, payload: Any = Body(None)):
    # TODO: work on logging
    logger.info("Received payload: %s", payload)

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
