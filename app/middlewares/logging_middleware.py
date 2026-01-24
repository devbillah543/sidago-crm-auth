from fastapi import Request
from config.logger import logger

async def logging_middleware(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        logger.error(str(e))
        return {"error": "Internal Server Error"}
