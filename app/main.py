from fastapi import FastAPI

from .routers import telegram, whatsapp

app = FastAPI(docs_url=None, redoc_url=None)
app.include_router(telegram.router)
app.include_router(whatsapp.router)
