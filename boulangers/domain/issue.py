from pydantic import BaseModel
from typing import Optional
from datetime import date


class Issue(BaseModel):
    key: str
    summary: str
    description: str = ''
    status: str = ''
    assignee: str = 'Unassigned'
    type: str = 'Issue'
    start_date: Optional[date] = None  # 시작일 추가
    due_date: Optional[date] = None  # 종료일 추가
