# application/ports.py

from abc import ABC, abstractmethod
from typing import List
from boulangers.domain.issue import Issue


class IssueRepositoryPort(ABC):
    @abstractmethod
    async def fetch_issues(self, jql_query: str) -> List[Issue]:
        pass
