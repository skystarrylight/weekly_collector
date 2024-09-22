from pydantic import BaseModel
from typing import Optional, List
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
    reporter: Optional[str] = None  # 이슈를 만든 사람
    priority: Optional[str] = None  # 우선순위
    parent: Optional[str] = None  # 부모 이슈 (있는 경우)
    subtasks: Optional[List[str]] = []  # 서브태스크 리스트 (있는 경우)
    created: Optional[date] = None  # 이슈 생성일
    updated: Optional[date] = None  # 마지막 업데이트 날짜
    time_spent: Optional[int] = None  # 이슈 작업에 소요된 시간 (초 단위)
    components: Optional[List[str]] = []  # 컴포넌트 (있는 경우)
    labels: Optional[List[str]] = []  # 라벨 (있는 경우)
