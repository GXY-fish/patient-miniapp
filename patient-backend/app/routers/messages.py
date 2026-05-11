from typing import List

from fastapi import APIRouter

from app.schemas.common import MessageResponse

router = APIRouter(prefix="/messages", tags=["messages"])

MESSAGES = [
    {"id": 1, "title": "医生已回复", "content": "请查看最新报告。", "time": "10:45", "unread": True},
    {"id": 2, "title": "随访提醒", "content": "请于本周内重新上传造口图片。", "time": "昨天", "unread": False},
]


@router.get("", response_model=List[MessageResponse])
def list_messages():
    return MESSAGES
