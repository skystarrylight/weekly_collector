import aiohttp
from aiohttp import BasicAuth
from typing import List, Dict, Optional
from boulangers.domain.issue import Issue
from boulangers.application.ports import IssueRepositoryPort
from datetime import datetime


class JiraClient(IssueRepositoryPort):
    def __init__(self, domain: str, email: str, api_token: str, epic_field: str = '"Epic Link"') -> None:
        """Jira 클라이언트 초기화."""
        self.base_url = f'https://{domain}.atlassian.net/rest/api/3'
        self.auth = BasicAuth(email, api_token)
        self.epic_field = epic_field

    async def fetch_issues(self, jql_query: str) -> List[Issue]:
        """
        Jira API로부터 이슈를 조회하고, Issue 객체 리스트로 변환.

        Args:
            jql_query (str): Jira 쿼리 언어(JQL)를 사용한 검색 조건.

        Returns:
            List[Issue]: 조회된 이슈들의 리스트.
        """
        search_url = f'{self.base_url}/search'
        params = {'jql': jql_query, 'maxResults': 1000}

        async with aiohttp.ClientSession(auth=self.auth) as session:
            async with session.get(search_url, params=params) as response:
                response.raise_for_status()
                data = await response.json()
                return [self._parse_issue(issue_data) for issue_data in data.get('issues', [])]

    @staticmethod
    def _parse_issue(self, issue_data: Dict) -> Issue:
        """
        Jira API로부터 받은 이슈 데이터를 Issue 객체로 변환.
        Args:
            issue_data (Dict): 이슈 데이터 JSON.
        Returns:
            Issue: 파싱된 이슈 객체.
        """
        fields = issue_data.get('fields', {})

        # 미리 정의한 필드와 Jira JSON의 필드를 동적으로 매핑
        field_map = {
            'key': issue_data.get('key', ''),
            'summary': fields.get('summary', ''),
            'description': self._parse_description(fields.get('description')),
            'status': fields.get('status', {}).get('name', ''),
            'assignee': fields.get('assignee', {}).get('displayName', ''),
            'reporter': fields.get('reporter', {}).get('displayName', ''),
            'priority': fields.get('priority', {}).get('name', ''),
            'type': fields.get('issuetype', {}).get('name', ''),
            'parent': fields.get('parent', {}).get('key', None),
            'subtasks': [subtask.get('key') for subtask in fields.get('subtasks', [])],
            'start_date': self._parse_date(fields.get('customfield_10015')),
            'due_date': self._parse_date(fields.get('duedate')),
            'created': self._parse_date(fields.get('created')),
            'updated': self._parse_date(fields.get('updated')),
            'time_spent': fields.get('timespent', None),
            'components': [component.get('name') for component in fields.get('components', [])],
            'labels': fields.get('labels', [])
        }

        # **kwargs를 사용하여 동적으로 Issue 객체 생성
        return Issue(**field_map)

    @staticmethod
    def _parse_description(description_info: Optional[Dict]) -> str:
        """
        중첩된 description 필드를 안전하게 파싱.

        Args:
            description_info (Optional[Dict]): description JSON 데이터.

        Returns:
            str: 파싱된 description 문자열.
        """
        if not description_info:
            return ''
        return ' '.join(paragraph.get('text', '') for content in description_info.get('content', [])
                        for paragraph in content.get('content', []))

    @staticmethod
    def _parse_date(date_str: Optional[str]) -> Optional[datetime]:
        """
        날짜 문자열을 안전하게 파싱.

        Args:
            date_str (Optional[str]): 날짜 문자열.

        Returns:
            Optional[datetime]: 파싱된 날짜 객체 또는 None.
        """
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else None
        except (ValueError, TypeError):
            return None