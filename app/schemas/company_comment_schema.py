from pydantic import BaseModel

class CommentRequest(BaseModel):
    message: str