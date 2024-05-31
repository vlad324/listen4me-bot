import logging
import sys

from fastapi import FastAPI

logger = logging.getLogger("transcribe-bot")
logger.setLevel(logging.DEBUG)

console_log_handler = logging.StreamHandler(sys.stdout)
console_log_handler.setFormatter(logging.Formatter("%(asctime)s.%(msecs)03.0f [%(threadName)s] %(levelname)s %(module)s - %(message)s",
                                                   "%Y-%m-%d %H:%M:%S"))
logger.addHandler(console_log_handler)

app = FastAPI(docs_url=None, redoc_url=None)


@app.get("/healthcheck")
def healthcheck():
    return {"status": "ok"}
