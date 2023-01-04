from typing import List

from application.core.database import get_db
from application.message.database import repository
from application.message.model.message import Message
from application.shared.base_router import BaseRouter
from fastapi import APIRouter, Depends, FastAPI
from sqlalchemy.orm import Session


class MessageRouter(BaseRouter):
  message_router = APIRouter()

  def __init__(self, prefix: str, app: FastAPI, dependencies: List[Depends] = None):
    super().__init__(prefix, app, dependencies)
  
  def route(self) -> APIRouter():
    return self.message_router

  @classmethod
  @message_router.get("/")
  async def get_messages_from_call(call_id: str, db: Session = Depends(get_db)) -> List[Message]:
    return repository.get_messages_from_call(db, call_id)

  @classmethod
  @message_router.post("/")
  async def send_message(message: Message, db: Session = Depends(get_db)) -> Message:
    return repository.send_message(db, message)

  @classmethod
  @message_router.delete("/")
  async def delete_message(message_id: str, db: Session = Depends(get_db)) -> Message:
    return repository.delete_message(db, message_id)