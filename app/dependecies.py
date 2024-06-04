import logging
import os
import sys

from openai import OpenAI


def get_console_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    console_log_handler = logging.StreamHandler(sys.stdout)
    console_log_handler.setFormatter(logging.Formatter("%(asctime)s.%(msecs)03.0f [%(threadName)s] %(levelname)s %(module)s - %(message)s",
                                                       "%Y-%m-%d %H:%M:%S"))
    logger.addHandler(console_log_handler)

    return logger


client = OpenAI(api_key=os.getenv("OPEN_AI_API_KEY"))


def transcribe_audio(file_name: str, file_content: bytes) -> str:
    transcription = client.audio.transcriptions.create(model="whisper-1", file=(file_name, file_content))
    return transcription.text
