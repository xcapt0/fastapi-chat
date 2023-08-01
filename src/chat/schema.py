from datetime import datetime
from pydantic import BaseModel, Field

from .utils import generate_color


class ChatDataSchema(BaseModel):
    timestamp: float = Field(default_factory=lambda: datetime.now().timestamp())
    color: str = Field(default_factory=generate_color)
    author: str
    text: str


class ChatSchema(BaseModel):
    type: str = Field('message', const=True)
    data: ChatDataSchema
