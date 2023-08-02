from datetime import datetime
from pydantic import BaseModel, Field


class ChatDataSchema(BaseModel):
    timestamp: float = Field(default_factory=lambda: datetime.now().timestamp())
    color: str
    author: str
    text: str


class ChatSchema(BaseModel):
    type: str = Field('message', const=True)
    data: ChatDataSchema
