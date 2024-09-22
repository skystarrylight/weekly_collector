from pydantic import BaseModel
from typing import Optional, List
from datetime import date


class Issue(BaseModel):
    key: str
    summary: str
    description: str = ''
    status: str = ''
    assignee: str = 'Unassigned'
    reporter: str = 'Unknown'
    priority: str = 'Medium'
    type: str = 'Issue'
    parent: Optional[str] = None
    subtasks: List[str] = []
    start_date: Optional[date] = None
    due_date: Optional[date] = None
    created: Optional[date] = None
    updated: Optional[date] = None
    time_spent: Optional[int] = None
    components: List[str] = []
    labels: List[str] = []