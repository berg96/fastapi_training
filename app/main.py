from fastapi import FastAPI

from app.api.endpoints import router

app = FastAPI()

# Подключаем роутер к приложению.
app.include_router(router)
