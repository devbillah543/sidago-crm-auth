from fastapi import FastAPI
from routes.api import router
from app.middlewares.logging_middleware import logging_middleware
from database.db import Base, engine

# 👇 IMPORT MODELS (THIS IS THE KEY FIX)
from app.models.user import User
from app.models.role import Role

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.middleware("http")(logging_middleware)
app.include_router(router, prefix="/api")
