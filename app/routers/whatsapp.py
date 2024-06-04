import os
from typing import Any, Annotated

import requests
from fastapi import BackgroundTasks, Body, Query, HTTPException, APIRouter

from ..dependecies import transcribe_audio, get_console_logger

router = APIRouter(prefix="/whatsapp", tags=["whatsapp"])

logger = get_console_logger("transcribe-bot-whatsapp")

phone_number_id = os.getenv("WA_PHONE_NUMBER_ID")
api_key = os.getenv("WA_API_KEY")
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}
wa_verify_token = os.getenv("WA_VERIFY_TOKEN")


def load_file_content(url):
    r = requests.get(url, headers={"Authorization": f"Bearer {api_key}"})
    r.raise_for_status()
    return r.content


class AudioProcessingTask:
    def __init__(self, wa_id: str, audio_id: str, message_id: str):
        self.wa_id = wa_id
        self.audio_id = audio_id
        self.message_id = message_id


# todo: make this more robust, handle errors and retries
def process_audio(task: AudioProcessingTask) -> None:
    response = requests.get(f"https://graph.facebook.com/v18.0/{task.audio_id}", headers=headers)
    response.raise_for_status()
    response_json = response.json()
    url = response_json["url"]
    file_type = response_json["mime_type"].split("/")[-1]

    file_content = load_file_content(url)

    transcription = transcribe_audio(f"file.{file_type}", file_content)
    send_message(task.wa_id, transcription, task.message_id)


def mark_message_as_read(message_id: str) -> None:
    body = {
        "messaging_product": "whatsapp",
        "status": "read",
        "message_id": message_id
    }
    response = requests.post(f"https://graph.facebook.com/v18.0/{phone_number_id}/messages", headers=headers, json=body)
    response.raise_for_status()


def send_message(wa_id: str, text: str, message_id: str | None = None) -> None:
    if message_id:
        body = {
            "messaging_product": "whatsapp",
            "recipient_type:": "individual",
            "to": wa_id,
            "type": "text",
            "text": {
                "body": text
            },
            "context": {
                "message_id": message_id
            }
        }
    else:
        body = {
            "messaging_product": "whatsapp",
            "recipient_type:": "individual",
            "to": wa_id,
            "type": "text",
            "text": {
                "body": text
            }
        }
    response = requests.post(f"https://graph.facebook.com/v18.0/{phone_number_id}/messages", headers=headers, json=body)
    response.raise_for_status()


@router.get("/l4me_bot/webhook")
async def handle_webhook_validation(mode: Annotated[str, Query(alias="hub.mode")],
                                    verify_token: Annotated[str, Query(alias="hub.verify_token")],
                                    challenge: Annotated[int, Query(alias="hub.challenge")]):
    if mode != "subscribe" or verify_token != wa_verify_token:
        raise HTTPException(status_code=400, detail="Invalid mode or token provided")

    return challenge


@router.post("/l4me_bot/webhook")
async def handle_webhook(background_tasks: BackgroundTasks, payload: Any = Body(None)):
    value = payload["entry"][0]["changes"][0]["value"]
    if value.get("statuses"):
        logger.debug("Received status change: %s", value["statuses"])
        pass
    elif value.get("messages"):
        message = value["messages"][0]
        wa_id = message["from"]
        message_type = message["type"]
        message_id = message["id"]

        mark_message_as_read(message_id)
        if message_type == "text":
            send_message(wa_id, "Hello there! 👋 Send or forward me a voice message and I will transcribe it for you.")
        elif message_type == "audio":
            background_tasks.add_task(process_audio, AudioProcessingTask(wa_id, message["audio"]["id"], message_id))
        else:
            raise HTTPException(status_code=400, detail="Unknown message type")

    else:
        raise HTTPException(status_code=400, detail="Unknown webhook request type")

    return {}
