# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.api import router
from app.middlewares.logging_middleware import logging_middleware
from database.db import Base, engine

# 👇 Import models to create tables
from app.models.user import User
from app.models.role import Role
from app.models.token import UserToken

app = FastAPI(title="Sidago CRM API")

# ------------------- Create tables -------------------
Base.metadata.create_all(bind=engine)

# ------------------- Add Logging Middleware -------------------
app.middleware("http")(logging_middleware)

# ------------------- CORS Setup -------------------
origins = [
    "*",  # For development: allow all origins
    # You can restrict to frontend URL in production, e.g.
    # "http://localhost:3000",
    # "https://your-frontend-domain.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------- Include API router -------------------
app.include_router(router, prefix="/api")
